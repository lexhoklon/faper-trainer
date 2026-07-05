import asyncio
import os
import signal
import subprocess
import threading
import time
from playwright.async_api import async_playwright

BRAVE_PATH = "/usr/bin/brave"

class Spotify:

    def __init__(self):
        self._browser = None
        self._page = None
        self._loop = None
        self._hilo = None
        self._proceso_brave = None
        self.cancion_actual = ""
        self.reproduciendo = False

    def _lanzar_brave(self):
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
            start_new_session=True
        )
        time.sleep(2)

    def iniciar_con_link(self, url):
        self._lanzar_brave()
        self._hilo = threading.Thread(
            target=self._arrancar_loop,
            args=(url,),
            daemon=True
        )
        self._hilo.start()

    def _arrancar_loop(self, url):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._reproducir(url))

    async def _reproducir(self, url):
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

            # Clic en el botón grande de reproducir la playlist
            # aria-label contiene el nombre de la playlist, usamos *=
            boton = self._page.locator("button[aria-label*='Reproducir']:not([aria-label*='de '])").first
            await boton.click(force=True)
            print("Clic en Reproducir!")

            await self._page.wait_for_timeout(2000)
            print("Reproduciendo!")

            self.reproduciendo = True
            await self._monitorear()

    async def _monitorear(self):
        """Obtiene el nombre de la canción actual cada 2 segundos."""
        while self.reproduciendo:
            try:
                info = await self._page.evaluate("""
                    () => {
                        const titulo = document.querySelector('[data-testid="context-item-link"]');
                        const artista = document.querySelector('[data-testid="context-item-info-subtitles"] a');
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
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(coro, self._loop)

    def play_pause(self):
        self._correr(self._click_boton("button[aria-label='Reproducir'], button[aria-label='Pausar']"))

    def siguiente(self):
        self._correr(self._click_boton("button[aria-label='Siguiente']"))

    def anterior(self):
        self._correr(self._click_boton("button[aria-label='Anterior']"))

    async def _click_boton(self, selector):
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
                // El slider de volumen de Spotify va de 0 a 1
                const sliders = document.querySelectorAll('input[type="range"]');
                const volSlider = Array.from(sliders).find(s => 
                    s.min === '0' && s.max === '1'
                );
                if (volSlider) {{
                    // Cambiamos el valor y disparamos eventos para que Spotify lo detecte
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value'
                    ).set;
                    nativeInputValueSetter.call(volSlider, {nivel});
                    volSlider.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    volSlider.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """)

    def bajar_volumen(self):
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._set_volumen(0.25), self._loop)

    def subir_volumen(self):
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._set_volumen(1.0), self._loop)

    def detener(self):
        self.reproduciendo = False
        if self._browser:
            self._correr(self._browser.close())
        self._cerrar_brave()

    def _cerrar_brave(self):
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
