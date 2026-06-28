from speaker import Speaker
import time
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
        self.activo = False            
        self.ejercicio_actual = ""
        self.tiempo_restante = 0
        self.speaker = Speaker()


    def iniciar(self):
        if self.activo:
            return
        self.activo = True
        self.speaker.hablar("Empezamos")
        self.cuenta_regresiva(3)
        self.speaker.hablar("Calentamiento")
        self.contar(*calentamiento)
        
        for ronda in range(rondas):
            if not self.activo:
                return
            print(f"\n===== RONDA {ronda + 1} =====")
            self.speaker.hablar(f"Ronda {ronda + 1}")
            for ejercicio in ejercicios:
                if not self.activo:
                    return
                nombre, tiempo = ejercicio
                self.speaker.hablar(nombre)
                self.cuenta_regresiva(3)
                self.contar(nombre, tiempo)
                self.ultimos_tres()
                self.speaker.hablar("Descanso")
                self.contar(*descanso)
            if ronda < rondas - 1:
                if not self.activo:
                    return
                self.speaker.hablar("Recuperacion")
                self.contar(*recuperacion)
        self.speaker.hablar("Estiramiento final")
        self.contar(*estiramiento)
        self.ejercicio_actual = "Entrenamiento finalizado"
        self.tiempo_restante = 0
        self.activo = False
        
    
    def detener(self):
        self.activo = False
        print("Entrenamiento detenido")


    def contar(self, nombre, tiempo):
        self.ejercicio_actual = nombre
        while tiempo > 0 and self.activo:
            self.tiempo_restante = tiempo
            print(tiempo)
            time.sleep(1)
            tiempo -= 1

            
    def cuenta_regresiva(self, segundos):
        for i in range(segundos, 0, -1):
            if not self.activo:
                return
            self.speaker.hablar(str(i))
            time.sleep(1)

            
    def ultimos_tres(self):
        if not self.activo:
            return
        self.speaker.hablar("Últimos tres segundos")
        for i in range(3, 0, -1):
            if not self.activo:
                return
            self.speaker.hablar(str(i))
            time.sleep(1)
