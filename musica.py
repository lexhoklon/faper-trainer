import asyncio
import os
import signal
import subprocess
import threading
import time
from playwright.async_api import async_playwright

BRAVE_PATH = "/usr/bin/brave"

class Musica:

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._page = None
        self._loop = None
        self._hilo = None
        self._proceso_brave = None
        self.cancion_actual = ""
        self.reproduciendo = False

    # ──────────────────────────────────────────────────────────
    # Lanzamiento de Brave (compartido por búsqueda y por link)
    # ──────────────────────────────────────────────────────────
    def _lanzar_brave(self):
        """
        Registra una regla de bspwm ANTES de abrir la ventana para que
        bspwm la marque como flotante + oculta en el instante en que se
        crea. Esto evita la condición de carrera de usar `bspc node`
        (sin selector) después de un time.sleep(), que depende de que
        la ventana ya tenga el foco en ese momento exacto.
        """
        subprocess.run(
            ["bspc", "rule", "-a", "Brave-browser", "-o",
             "state=floating", "hidden=on"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        self._proceso_brave = subprocess.Popen(
            [BRAVE_PATH, "--remote-debugging-port=9222",
             "--new-window", "--window-size=1,1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # crea su propio grupo de procesos
                                     # para poder matarlo entero después
        )
        # Pequeño margen para que el puerto de debugging quede escuchando
        # antes de que Playwright intente conectarse.
        time.sleep(2)

    def iniciar(self, busqueda):
        self._lanzar_brave()

        self._hilo = threading.Thread(
            target=self._arrancar_loop,
            args=(busqueda,),
            daemon=True
        )
        self._hilo.start()

    def _arrancar_loop(self, busqueda):
        """
        Crea el event loop de asyncio en el hilo dedicado
        y lanza la búsqueda.
        """
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._buscar_y_reproducir(busqueda))

    async def _buscar_y_reproducir(self, busqueda):
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            self._browser = browser
            context = browser.contexts[0]
            self._page = await context.new_page()
            await self._page.set_viewport_size({"width": 1280, "height": 800})

            url = f"https://music.youtube.com/search?q={busqueda.replace(' ', '+')}"
            print(f"Navegando a: {url}")
            await self._page.goto(url)
            await self._page.wait_for_load_state("networkidle")
            await self._page.wait_for_timeout(3000)
            print("Página cargada!")

            boton = self._page.locator("yt-button-shape button[aria-label='Reproducir']")
            await boton.first.click(force=True)
            print("Clic en Reproducir!")

            await self._page.wait_for_timeout(3000)
            print("Reproduciendo!")

            self.reproduciendo = True
            await self._monitorear()

    def iniciar_con_link(self, url):
        """Reproduce directamente desde un link de YT Music."""
        self._lanzar_brave()

        self._hilo = threading.Thread(
            target=self._arrancar_loop_link,
            args=(url,),
            daemon=True
        )
        self._hilo.start()

    def _arrancar_loop_link(self, url):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._reproducir_link(url))

    async def _reproducir_link(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            self._browser = browser
            context = browser.contexts[0]
            self._page = await context.new_page()
            await self._page.set_viewport_size({"width": 1280, "height": 800})

            print(f"Navegando a: {url}")
            await self._page.goto(url)
            await self._page.wait_for_load_state("networkidle")
            await self._page.wait_for_timeout(3000)
            print("Página cargada!")

            # El botón de play cambia según el tipo de link:
            # - canción individual  -> barra inferior (#play-pause-button)
            # - playlist / álbum    -> "Reproducir todo" (ytmusic-play-button-renderer)
            # - resultado de búsqueda -> botón que aparece al hover
            # Probamos en ese orden con CLICS REALES de Playwright, porque
            # un clic disparado por page.evaluate()/JS NO cuenta como gesto
            # de usuario para Chrome y su política de autoplay bloquea el
            # audio silenciosamente (esta era la causa de que "cargue pero
            # no suene nada").
            selectores_posibles = [
                # Botón circular grande del encabezado de playlist/álbum.
                # El aria-label varía ("Reproducir", "Reproducir todo",
                # "Reproducir mezcla"...), así que buscamos por texto
                # parcial en vez de una etiqueta exacta.
                "ytmusic-play-button-renderer button",
                # Barra inferior del reproductor (canción individual)
                "#play-pause-button",
                # Cualquier otro botón de play visible en la página
                # (cubre además resultados de búsqueda tipo hover)
                "button[aria-label*='Reproducir' i]:visible",
            ]

            clic_exitoso = False
            for selector in selectores_posibles:
                try:
                    boton = self._page.locator(selector).first
                    await boton.wait_for(state="visible", timeout=4000)
                    await boton.click(force=True)
                    clic_exitoso = True
                    print(f"Clic en: {selector}")
                    break
                except Exception:
                    continue

            if not clic_exitoso:
                print("No se encontró botón de reproducción con los selectores conocidos.")

            await self._page.wait_for_timeout(2000)

            # Verificación final: si el <video> sigue pausado, intentamos
            # un segundo clic real sobre la barra inferior.
            try:
                pausado = await self._page.evaluate("""
                    () => {
                        const v = document.querySelector('video');
                        return v ? v.paused : true;
                    }
                """)
                if pausado:
                    print("Seguía pausado, reintentando con la barra inferior...")
                    boton_barra = self._page.locator("#play-pause-button").first
                    await boton_barra.click(force=True, timeout=4000)
            except Exception as e:
                print(f"No se pudo verificar/forzar reproducción: {e}")

            print("Reproduciendo!")
            self.reproduciendo = True
            await self._monitorear()

    async def _monitorear(self):
        while self.reproduciendo:
            try:
                info = await self._page.evaluate("""
                    () => {
                        const titulo = document.querySelector('.title.ytmusic-player-bar');
                        const artista = document.querySelector('.byline.ytmusic-player-bar a');
                        return {
                            titulo: titulo ? titulo.innerText.trim() : '',
                            artista: artista ? artista.innerText.trim() : ''
                        }
                    }
                """)
                if info['titulo']:
                    self.cancion_actual = f"{info['titulo']} — {info['artista']}"
            except:
                pass
            await asyncio.sleep(2)

    def _correr(self, coro):
        """Ejecuta una corrutina en el loop dedicado desde fuera."""
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(coro, self._loop)

    def play_pause(self):
        """Alterna entre play y pause."""
        self._correr(self._click_boton("yt-icon-button button[aria-label='Reproducir'], yt-icon-button button[aria-label='Pausar']"))

    def siguiente(self):
        """Salta a la siguiente canción."""
        self._correr(self._click_boton("button[aria-label='Siguiente']"))

    def anterior(self):
        """Vuelve a la canción anterior."""
        self._correr(self._click_boton("button[aria-label='Anterior']"))

    async def _click_boton(self, selector):
        """Controla el reproductor via JavaScript directamente."""
        try:
            await self._page.evaluate(f"""
                () => {{
                    const btn = document.querySelector("{selector}");
                    if (btn) btn.click();
                }}
            """)
        except Exception as e:
            print(f"Error: {e}")

    async def _set_volumen(self, nivel):
        await self._page.evaluate(f"""
            () => {{
                const video = document.querySelector('video');
                if (video) {{
                    video.volume = {nivel};
                    video.muted = false;
                }}
                // Dispara evento para que YT Music sincronice su UI
                video.dispatchEvent(new Event('volumechange'));
            }}
        """)

    def bajar_volumen(self):
        """Llamado cuando la IA va a hablar — baja música a 25%."""
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._set_volumen(0.25), self._loop)

    def subir_volumen(self):
        """Llamado cuando la IA termina de hablar — sube música a 100%."""
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._set_volumen(1.0), self._loop)

    def detener(self):
        self.reproduciendo = False

        if self._browser:
            self._correr(self._browser.close())

        self._cerrar_brave()

    def _cerrar_brave(self):
        """
        Mata el proceso de Brave que lanzamos (y todos sus hijos).

        browser.close() sobre una conexión CDP (connect_over_cdp) solo
        desconecta a Playwright del navegador remoto, NO lo cierra —
        Playwright no fue quien lo lanzó, nosotros sí con subprocess.
        Por eso el proceso quedaba vivo (había que usar pkill a mano).

        Lanzamos Brave con start_new_session=True para que quede como
        líder de su propio grupo de procesos, así podemos matar todo
        el árbol (ventana + procesos hijos de Chromium) de una sola vez.
        """
        if self._proceso_brave and self._proceso_brave.poll() is None:
            try:
                pgid = os.getpgid(self._proceso_brave.pid)
                os.killpg(pgid, signal.SIGTERM)
                self._proceso_brave.wait(timeout=3)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(pgid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

        self._proceso_brave = None
