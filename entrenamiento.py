from speaker import Speaker
import time
import threading
import progreso
from workout import (
    calentamiento,
    descanso,
    recuperacion,
    estiramiento,
    rondas,
    rutinas,
    es_dia_descanso,
)


class Entrenamiento:

    def __init__(self):
        self._activo = threading.Event()
        self.ejercicio_actual = ""
        self.tiempo_restante = 0
        self.speaker = Speaker()

        # Al crear el objeto, ya calculamos qué rutina toca hoy
        # Guardamos el índice para poder guardar el progreso al terminar
        self.indice_actual, self.rutina_actual = progreso.rutina_de_hoy(rutinas)

    @property
    def activo(self):
        return self._activo.is_set()

    def iniciar(self):
        if self.activo:
            return

        # Si hoy es día de descanso, no hace nada
        if es_dia_descanso():
            self.ejercicio_actual = "Día de descanso 💤"
            return

        self._activo.set()
        nombre_rutina = self.rutina_actual["nombre"]

        self.speaker.hablar(f"Comenzamos rutina de {nombre_rutina}")
        self.speaker.esperar()
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
        self.speaker.esperar()
        self.contar(*calentamiento)

    def _fase_rondas(self):
        for ronda in range(rondas):
            if not self.activo:
                return
            print(f"\n===== RONDA {ronda + 1} =====")
            self.speaker.hablar(f"Ronda {ronda + 1}")
            self.speaker.esperar()
            self._fase_ejercicios()
            if ronda < rondas - 1:
                self._anunciar_y_contar("Recuperación", *recuperacion)

    def _fase_ejercicios(self):
        # Toma los ejercicios de la rutina actual
        for nombre, tiempo in self.rutina_actual["ejercicios"]:
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

        # Ahora le pasamos también el nombre de la rutina
        progreso.guardar(self.indice_actual, self.rutina_actual["nombre"])

    # ── helpers ────────────────────────────────────────────

    def _anunciar_y_contar(self, anuncio, nombre, tiempo):
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
