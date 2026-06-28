from datetime import datetime

# ── Tiempos globales ────────────────────────────────────────
# Estos se reusan en todas las rutinas para que sean consistentes

calentamiento = ("Calentamiento", 300)   # 5 minutos
descanso      = ("Descanso", 15)         # 15 segundos entre ejercicios
recuperacion  = ("Recuperación", 60)     # 1 minuto entre rondas
estiramiento  = ("Estiramiento", 300)    # 5 minutos
rondas        = 4

# ── Rutinas ─────────────────────────────────────────────────
# Cada rutina es un diccionario con nombre y lista de ejercicios.

rutinas = [
    {
        "nombre": "Full Body",
        "ejercicios": [
            ("Sentadilla con elevación de rodilla", 45),
            ("Shadow Boxing", 45),
            ("Step Touch", 45),
            ("Flexiones contra pared", 45),
            ("Mini Burpees", 45),
        ]
    },
    {
        "nombre": "Tronco Superior",
        "ejercicios": [
            ("Flexiones contra pared", 45),
            ("Shadow Boxing", 45),
            ("Rodilla al Codo", 45),
            ("Plancha", 45),
            ("Golpes Arriba", 45),
        ]
    },
    {
        "nombre": "Tronco Inferior",
        "ejercicios": [
            ("Sentadilla clásica", 45),
            ("Zancada atrás alternada", 45),
            ("Peso muerto sin peso", 45),
            ("Elevación de pantorrillas", 45),
            ("Sentadilla de pared", 45),
        ]
    },
]

# ── Días de descanso ─────────────────────────────────────────
# Si hoy es uno de estos días, la app mostrará "Día de descanso"
DIAS_DESCANSO = ["Tuesday", "Friday"]  # Martes y Viernes

def es_dia_descanso():
    """Retorna True si hoy es día de descanso."""
    hoy = datetime.now().strftime("%A")  # Ej: "Monday", "Tuesday"
    return hoy in DIAS_DESCANSO
