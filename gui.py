import threading
import tkinter as tk
import calendar
from datetime import datetime
from entrenamiento import Entrenamiento
from workout import es_dia_descanso, rutinas
from musica import Musica
musica = Musica()
import progreso

entrenamiento = Entrenamiento()
entrenamiento.speaker.musica = musica
hilo = None
ventana_cal = None
ventana_historial = None  
ventana_peso = None  


def iniciar():
    global hilo
    if hilo and hilo.is_alive():
        return
    hilo = threading.Thread(target=entrenamiento.iniciar, daemon=True)
    hilo.start()


def detener():
    entrenamiento.detener()


def actualizar_labels():
    label_ejercicio.config(text=entrenamiento.ejercicio_actual)
    label_tiempo.config(text=str(entrenamiento.tiempo_restante))
    ventana.after(200, actualizar_labels)


def marcar_descanso():
    registrado = progreso.registrar_descanso()
    if registrado:
        label_ejercicio.config(text="Descanso registrado ✅")
    else:
        label_ejercicio.config(text="Ya registraste el descanso hoy")


def abrir_calendario():
    global ventana_cal

    # SI ya esta abierto, solo lo trae al frente en vez de abrir otro
    if ventana_cal and ventana_cal.winfo_exists():
        ventana_cal.lift()
        return

    datos = progreso.cargar()
    entrenamientos = datos.get("entrenamientos", {})
    descansos = datos.get("descansos", [])

    hoy = datetime.now()
    anio, mes = hoy.year, hoy.month
    hoy_str = hoy.strftime("%Y-%m-%d")

    ventana_cal = tk.Toplevel(ventana)
    ventana_cal.title("Progreso del mes")
    ventana_cal.configure(bg="black")
    ventana_cal.resizable(False, False)

    nombre_mes = hoy.strftime("%B %Y")
    tk.Label(
        ventana_cal,
        text=nombre_mes,
        font=("Arial", 16, "bold"),
        fg="white",
        bg="black"
    ).grid(row=0, column=0, columnspan=7, pady=10)

    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for col, dia in enumerate(dias_semana):
        tk.Label(
            ventana_cal,
            text=dia,
            font=("Arial", 10, "bold"),
            fg="gray",
            bg="black",
            width=5
        ).grid(row=1, column=col, padx=2)

    cal = calendar.monthcalendar(anio, mes)

    for fila, semana in enumerate(cal):
        for col, dia in enumerate(semana):
            if dia == 0:
                tk.Label(ventana_cal, text="", bg="black", width=5).grid(
                    row=fila + 2, column=col, padx=2, pady=2
                )
                continue

            fecha_str = f"{anio}-{mes:02d}-{dia:02d}"

            if fecha_str == hoy_str:
                color = "blue"
                texto_color = "white"
            elif fecha_str in entrenamientos:
                color = "green"
                texto_color = "white"
            elif fecha_str in descansos:
                color = "gray"
                texto_color = "white"
            else:
                color = "#222222"
                texto_color = "white"

            tk.Label(
                ventana_cal,
                text=str(dia),
                font=("Arial", 11),
                fg=texto_color,
                bg=color,
                width=4,
                relief="flat",
                padx=4,
                pady=4
            ).grid(row=fila + 2, column=col, padx=2, pady=2)

    # Leyenda — va dentro de abrir_calendario, al final
    leyenda = [("🟢 Entrenó", "green"), ("😴 Descansó", "gray"), ("🔵 Hoy", "blue")]
    for i, (texto, color) in enumerate(leyenda):
        tk.Label(
            ventana_cal,
            text=texto,
            fg=color,
            bg="black",
            font=("Arial", 9)
        ).grid(row=len(cal) + 3, column=i * 2, columnspan=2, pady=8)


def abrir_historial():
    global ventana_historial

    # Si ya está abierta, la trae al frente
    if ventana_historial and ventana_historial.winfo_exists():
        ventana_historial.lift()
        return

    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial semanal")
    ventana_historial.configure(bg="black")
    ventana_historial.resizable(False, False)

    # Obtenemos el texto del resumen desde progreso.py
    resumen = progreso.resumen_semana_actual()

    tk.Label(
        ventana_historial,
        text=resumen,
        font=("Courier", 13),  # Courier para que el texto quede alineado
        fg="white",
        bg="black",
        justify="left",        # alineado a la izquierda
        padx=20,
        pady=20
    ).pack()


def abrir_registrar_peso():
    global ventana_peso

    if ventana_peso and ventana_peso.winfo_exists():
        ventana_peso.lift()
        return

    ventana_peso = tk.Toplevel(ventana)
    ventana_peso.title("Registrar peso")
    ventana_peso.configure(bg="black")
    ventana_peso.resizable(False, False)

    tk.Label(
        ventana_peso,
        text="¿Cuánto pesas hoy? (kg)",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="black"
    ).pack(pady=20)

    # Campo de texto para ingresar el peso
    entrada = tk.Entry(
        ventana_peso,
        font=("Arial", 20),
        width=8,
        justify="center"
    )
    entrada.pack(pady=10)
    entrada.focus()  # el cursor queda listo para escribir

    def guardar():
        texto = entrada.get().strip().replace(",", ".")  # acepta coma o punto
        try:
            peso = float(texto)
            progreso.registrar_peso(peso)
            ventana_peso.destroy()
            label_ejercicio.config(text=f"Peso registrado: {peso} kg ✅")
        except ValueError:
            # Si escribe algo que no es número, muestra error
            label_error.config(text="⚠️ Ingresa un número válido")

    label_error = tk.Label(
        ventana_peso,
        text="",
        fg="red",
        bg="black",
        font=("Arial", 10)
    )
    label_error.pack()

    tk.Button(
        ventana_peso,
        text="GUARDAR",
        command=guardar,
        width=12,
        height=2,
        bg="green",
        fg="white"
    ).pack(pady=15)


def abrir_historial_peso():
    global ventana_peso

    if ventana_peso and ventana_peso.winfo_exists():
        ventana_peso.lift()
        return

    ventana_peso = tk.Toplevel(ventana)
    ventana_peso.title("Historial de peso")
    ventana_peso.configure(bg="black")
    ventana_peso.resizable(False, False)

    resumen = progreso.historial_pesos()

    tk.Label(
        ventana_peso,
        text=resumen,
        font=("Courier", 13),
        fg="white",
        bg="black",
        justify="left",
        padx=20,
        pady=20
    ).pack()


ventana_musica = None

def abrir_musica():
    global ventana_musica

    if ventana_musica and ventana_musica.winfo_exists():
        ventana_musica.lift()
        return

    ventana_musica = tk.Toplevel(ventana)
    ventana_musica.title("Música")
    ventana_musica.configure(bg="black")
    ventana_musica.resizable(False, False)

    tk.Label(ventana_musica, text="🎵 Música",
             font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=10)

    # ── Búsqueda por texto ──
    tk.Label(ventana_musica, text="Buscar playlist:",
             font=("Arial", 11), fg="gray", bg="black").pack()
    entrada = tk.Entry(ventana_musica, font=("Arial", 14),
                       width=30, justify="center")
    entrada.pack(pady=5)
    entrada.insert(0, "workout playlist")
    entrada.focus()

    # ── O pegar link directo ──
    tk.Label(ventana_musica, text="— o pega un link de YT Music —",
             font=("Arial", 10), fg="gray", bg="black").pack(pady=5)
    entrada_link = tk.Entry(ventana_musica, font=("Arial", 11),
                            width=30, justify="center")
    entrada_link.pack(pady=5)

    # Label canción actual
    label_cancion = tk.Label(ventana_musica, text="Sin reproducir",
                             font=("Arial", 11), fg="gray", bg="black",
                             wraplength=300)
    label_cancion.pack(pady=5)

    def buscar():
        link = entrada_link.get().strip()
        texto = entrada.get().strip()
        if link:
            label_cancion.config(text="Cargando...")
            musica.iniciar_con_link(link)
        elif texto:
            label_cancion.config(text="Cargando...")
            musica.iniciar(texto)

    tk.Button(ventana_musica, text="▶ REPRODUCIR", command=buscar,
              width=20, height=2, bg="green", fg="white").pack(pady=10)

    # Controles
    frame_controles = tk.Frame(ventana_musica, bg="black")
    frame_controles.pack(pady=10)

    tk.Button(frame_controles, text="⏮", command=musica.anterior,
              width=5, height=2, bg="#1a1a2e", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(frame_controles, text="⏯", command=musica.play_pause,
              width=5, height=2, bg="#1a1a2e", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(frame_controles, text="⏭", command=musica.siguiente,
              width=5, height=2, bg="#1a1a2e", fg="white").grid(row=0, column=2, padx=5)

    def actualizar_cancion():
        if musica.cancion_actual:
            label_cancion.config(text=musica.cancion_actual, fg="white")
        if ventana_musica.winfo_exists():
            ventana_musica.after(2000, actualizar_cancion)

    actualizar_cancion()


def cerrar_app():
    """Se ejecuta al cerrar la ventana principal."""
    musica.detener()
    ventana.destroy()


def crear_ventana():
    global ventana, label_ejercicio, label_tiempo

    ventana = tk.Tk()
    ventana.title("Faper Trainer")
    ventana.geometry("800x600")
    ventana.configure(bg="black")

    # Frame central que contiene todo
    frame_central = tk.Frame(ventana, bg="black")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")  # centrado perfecto

    # ── Rutina de hoy ──────────────────────────────────────
    if es_dia_descanso():
        texto_rutina = "💤 Día de Descanso"
        color_rutina = "gray"
    else:
        _, rutina = progreso.rutina_de_hoy(rutinas)
        calorias = rutina["calorias"]
        texto_rutina = f"{rutina['nombre']}  🔥 ~{calorias} kcal"
        color_rutina = "yellow"

    tk.Label(
        frame_central,       # ← padre es frame_central, no ventana
        text=texto_rutina,
        font=("Arial", 20, "bold"),
        fg=color_rutina,
        bg="black"
    ).pack(pady=10)

    # ── Ejercicio actual ────────────────────────────────────
    label_ejercicio = tk.Label(
        frame_central,
        text="Listo",
        font=("Arial", 32, "bold"),
        fg="white",
        bg="black"
    )
    label_ejercicio.pack(pady=5)

    # ── Timer ───────────────────────────────────────────────
    label_tiempo = tk.Label(
        frame_central,
        text="0",
        font=("Arial", 100, "bold"),
        fg="green",
        bg="black"
    )
    label_tiempo.pack(pady=5)

    # ── Botones en grid 3x2 ─────────────────────────────────
    frame_botones = tk.Frame(frame_central, bg="black")
    frame_botones.pack(pady=15)

    estado_start = "disabled" if es_dia_descanso() else "normal"

    botones = [
        ("START",               iniciar,              estado_start, "#1a1a2e", "white"),
        ("STOP",                detener,              "normal",     "#1a1a2e", "white"),
        ("📅 CALENDARIO",      abrir_calendario,     "normal",     "#1a1a2e", "white"),
        ("📊 HISTORIAL",       abrir_historial,      "normal",     "#1a1a2e", "white"),
        ("⚖️ REGISTRAR PESO",  abrir_registrar_peso, "normal",     "#1a1a2e", "white"),
        ("📈 VER PESO",        abrir_historial_peso, "normal",     "#1a1a2e", "white"),
        ("🎵 MÚSICA",       abrir_musica,         "normal",     "#1a1a2e", "white"),
    ]

    if es_dia_descanso():
        botones[0] = ("😴 MARCAR DESCANSO", marcar_descanso, "normal", "gray", "white")

    for i, (texto, comando, estado, bg, fg) in enumerate(botones):
        fila = i // 3
        columna = i % 3
        tk.Button(
            frame_botones,
            text=texto,
            command=comando,
            width=18,
            height=2,
            state=estado,
            bg=bg,
            fg=fg
        ).grid(row=fila, column=columna, padx=8, pady=6)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)  # ← intercepta el cierre
    actualizar_labels()
    ventana.mainloop()


if __name__ == "__main__":
    crear_ventana()
