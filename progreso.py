import json
import os
from datetime import datetime

ARCHIVO = "progreso.json"

def cargar():
    if not os.path.exists(ARCHIVO):
        return {"indice": 0, "ultima_fecha": None, "descansos": []}
    with open(ARCHIVO, "r") as f:
        return json.load(f)


def guardar(indice, nombre_rutina):
    """
    Ahora también guarda el nombre de la rutina completada
    en el historial de entrenamientos.
    """
    datos = cargar()
    hoy = datetime.now().strftime("%Y-%m-%d")
    datos["indice"] = indice
    datos["ultima_fecha"] = hoy

    # Guardamos el historial de entrenamientos
    # "entrenamientos" es un dict donde la clave es la fecha
    if "entrenamientos" not in datos:
        datos["entrenamientos"] = {}
    datos["entrenamientos"][hoy] = nombre_rutina

    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=2)


def registrar_descanso():
    """
    Agrega la fecha de hoy a la lista de descansos.
    Si ya está registrada (apretó el botón dos veces), no la duplica.
    """
    progreso = cargar()
    hoy = datetime.now().strftime("%Y-%m-%d")

    if hoy not in progreso["descansos"]:
        progreso["descansos"].append(hoy)
        with open(ARCHIVO, "w") as f:
            json.dump(progreso, f, indent=2)
        return True   # se registró
    return False      # ya estaba registrado

def siguiente_indice(total_rutinas):
    progreso = cargar()
    indice_actual = progreso["indice"]
    return (indice_actual + 1) % total_rutinas

def rutina_de_hoy(rutinas):
    progreso = cargar()
    hoy = datetime.now().strftime("%Y-%m-%d")

    if progreso["ultima_fecha"] is None:
        indice = 0
    elif progreso["ultima_fecha"] == hoy:
        indice = progreso["indice"]
    else:
        indice = siguiente_indice(len(rutinas))

    return indice, rutinas[indice]
