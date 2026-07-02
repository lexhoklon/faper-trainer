import json
import os
from datetime import datetime, timedelta  # ← agrega timedelta

ARCHIVO = "progreso.json"

def cargar():
    if not os.path.exists(ARCHIVO):
        return {"indice": 0, "ultima_fecha": None, "descansos": []}
    with open(ARCHIVO, "r") as f:
        return json.load(f)


def guardar(indice, nombre_rutina):
    datos = cargar()
    hoy = datetime.now()
    hoy_str = hoy.strftime("%Y-%m-%d")

    # Calculamos el número de semana del año para agrupar
    # Ej: "2026-W27" → semana 27 del 2026
    semana_str = hoy.strftime("%Y-W%W")

    datos["indice"] = indice
    datos["ultima_fecha"] = hoy_str

    # Historial de entrenamientos por día (ya lo teníamos)
    if "entrenamientos" not in datos:
        datos["entrenamientos"] = {}
    datos["entrenamientos"][hoy_str] = nombre_rutina

    # Historial agrupado por semana (nuevo)
    if "semanas" not in datos:
        datos["semanas"] = {}
    if semana_str not in datos["semanas"]:
        datos["semanas"][semana_str] = {}
    datos["semanas"][semana_str][hoy_str] = nombre_rutina

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


def resumen_semana_actual():
    """
    Retorna un texto con el resumen de la semana actual.
    Incluye entrenamientos y descansos registrados.
    """
    datos = cargar()
    hoy = datetime.now()
    semana_str = hoy.strftime("%Y-W%W")

    semanas = datos.get("semanas", {})
    descansos = datos.get("descansos", [])
    semana_actual = semanas.get(semana_str, {})

    # Calculamos el lunes de esta semana
    lunes = hoy - timedelta(days=hoy.weekday())

    lineas = []
    lineas.append(f"Semana del {lunes.strftime('%d %b')} - {(lunes + timedelta(days=6)).strftime('%d %b %Y')}")
    lineas.append("─" * 35)

    # Recorremos los 7 días de la semana
    nombres_dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for i in range(7):
        dia = lunes + timedelta(days=i)
        dia_str = dia.strftime("%Y-%m-%d")
        nombre_dia = nombres_dias[i]
        fecha_corta = dia.strftime("%d %b")

        if dia_str in semana_actual:
            rutina = semana_actual[dia_str]
            lineas.append(f"{nombre_dia} {fecha_corta} → 💪 {rutina}")
        elif dia_str in descansos:
            lineas.append(f"{nombre_dia} {fecha_corta} → 😴 Descanso")
        elif dia <= hoy:
            lineas.append(f"{nombre_dia} {fecha_corta} → ⬜ Sin registrar")
        else:
            lineas.append(f"{nombre_dia} {fecha_corta} → ...")

    return "\n".join(lineas)


def registrar_peso(peso):
    """
    Guarda el peso del día de hoy en el historial.
    Si ya hay un peso registrado hoy, lo sobreescribe.
    """
    datos = cargar()
    hoy = datetime.now().strftime("%Y-%m-%d")

    if "pesos" not in datos:
        datos["pesos"] = {}

    datos["pesos"][hoy] = peso

    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=2)

def historial_pesos():
    """
    Retorna un texto con el historial de pesos registrados,
    ordenado del más reciente al más antiguo.
    """
    datos = cargar()
    pesos = datos.get("pesos", {})

    if not pesos:
        return "No hay pesos registrados aún."

    lineas = ["📈 Historial de peso", "─" * 25]

    # Ordenamos por fecha de más reciente a más antiguo
    for fecha in sorted(pesos.keys(), reverse=True):
        peso = pesos[fecha]
        # Convertimos "2026-07-01" a "01 Jul 2026" para que sea más legible
        fecha_bonita = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d %b %Y")
        lineas.append(f"{fecha_bonita} → {peso} kg")

    return "\n".join(lineas)
