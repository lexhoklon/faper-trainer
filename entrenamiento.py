from speaker import Speaker
import time
import threading
from workout import (
    calentamiento,
    ejercicios,
    descanso,
    recuperacion,
    estiramiento,
    rondas,
)


class Entrenamiento:

    def __init__(self):
        self._activo = threading.Event()
        self.ejercicio_actual = ""
        self.tiempo_restante = 0
        self.speaker = Speaker()

    @property
    def activo(self):
        return self._activo.is_set()

    def iniciar(self):
        if self.activo:
            return
        self._activo.set()
        self.speaker.hablar("Empezamos")
        self.speaker.esperar()  # ← espera que "Empezamos" termine
        self._fase_calentamiento()
        self._fase_rondas()
        self._fase_estiramiento()

    def detener(self):
        self._activo.clear()

    # ── fases ──────────────────────────────────────────────

    def _fase_calentamiento(self):
        if not self.activo:
            return
        self.speaker.hablar("Calentamiento")
        self.speaker.esperar()  # ← espera que "Calentamiento" termine
        self.contar(*calentamiento)  # ← y arranca el time
    
    def _fase_rondas(self):
        for ronda in range(rondas):
            if not self.activo:
                return
            print(f"\n===== RONDA {ronda + 1} =====")
            self.speaker.hablar(f"Ronda {ronda + 1}")
            self.speaker.esperar()  # ← espera el anuncio de ronda
            self._fase_ejercicios()
            if ronda < rondas - 1:
                self._anunciar_y_contar("Recuperación", *recuperacion)
    
    def _fase_ejercicios(self):
        for nombre, tiempo in ejercicios:
            if not self.activo:
                return
            self._anunciar_y_contar(nombre, nombre, tiempo)
            self._anunciar_y_contar("Descanso", *descanso)

    def _fase_estiramiento(self):
        if not self.activo:
            return
        self.speaker.hablar("Estiramiento final")
        self.speaker.esperar()
        self.contar(*estiramiento)
        self.ejercicio_actual = "Entrenamiento finalizado"
        self.tiempo_restante = 0
        self._activo.clear()

    # ── helpers ────────────────────────────────────────────

    def _anunciar_y_contar(self, anuncio, nombre, tiempo):
        """Anuncia, hace cuenta regresiva y empieza el timer."""
        if not self.activo:
            return
        self.speaker.hablar(anuncio)
        self.speaker.esperar()
        self.contar(nombre, tiempo)

    def contar(self, nombre, tiempo):
        self.ejercicio_actual = nombre
        ya_anuncio_tres = False
        while tiempo > 0 and self.activo:
            self.tiempo_restante = tiempo
            print(tiempo)
            if tiempo == 4 and not ya_anuncio_tres:
                self.speaker.hablar("Últimos tres segundos")
                ya_anuncio_tres = True
            time.sleep(1)
            tiempo -= 1
    
