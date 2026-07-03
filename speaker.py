import asyncio
import queue
import subprocess
import threading
import edge_tts

VOZ = "es-MX-DaliaNeural"

class Speaker:

    def __init__(self):
        self._cola = queue.Queue()
        self._hilo = threading.Thread(target=self._worker, daemon=True)
        self._hilo.start()
        self.musica = None  # ← referencia a Musica, se asigna desde gui.py

    def _worker(self):
        while True:
            texto = self._cola.get()
            if texto is None:
                break
            asyncio.run(self._reproducir(texto))
            self._cola.task_done()

    async def _reproducir(self, texto):
        # Bajamos volumen antes de hablar
        if self.musica:
            self.musica.bajar_volumen()

        communicate = edge_tts.Communicate(texto, VOZ)

        proc = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-f", "mp3", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                proc.stdin.write(chunk["data"])

        proc.stdin.close()
        proc.wait()

        # Subimos volumen después de hablar
        if self.musica:
            self.musica.subir_volumen()

    def hablar(self, texto):
        self._cola.put(texto)

    def esperar(self):
        self._cola.join()

    def detener(self):
        self._cola.put(None)
