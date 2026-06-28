import asyncio
import queue
import subprocess
import threading
import edge_tts

# La voz a usar — puedes cambiarla (ver más abajo)
VOZ = "es-MX-DaliaNeural"

class Speaker:

    def __init__(self):
        self._cola = queue.Queue()
        self._hilo = threading.Thread(target=self._worker, daemon=True)
        self._hilo.start()

    def _worker(self):
        """Hilo dedicado que consume la cola y reproduce cada texto."""
        while True:
            texto = self._cola.get()
            if texto is None:
                break
            asyncio.run(self._reproducir(texto))  # edge-tts es async, por eso usamos asyncio.run()
            self._cola.task_done()

    async def _reproducir(self, texto):
        """
        Pide el audio a edge-tts en chunks (streaming)
        y los va pasando directamente a ffplay para reproducirlos.
        Así no necesitamos guardar ningún archivo temporal.
        """
        communicate = edge_tts.Communicate(texto, VOZ)

        # Abrimos ffplay listo para recibir audio por stdin
        proc = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-f", "mp3", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,  # silenciamos la salida visual
            stderr=subprocess.DEVNULL,
        )

        # Recibimos los chunks de audio y los enviamos a ffplay en tiempo real
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                proc.stdin.write(chunk["data"])

        proc.stdin.close()
        proc.wait()  # esperamos a que ffplay termine de reproducir

    def hablar(self, texto):
        """Encola el texto — regresa inmediatamente, no bloquea."""
        self._cola.put(texto)

    def esperar(self):
        """Bloquea hasta que todo el audio pendiente termine de sonar."""
        self._cola.join()

    def detener(self):
        """Cierra el hilo worker limpiamente."""
        self._cola.put(None)
