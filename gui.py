import threading
import tkinter as tk
from tkinter import font as tkfont
import calendar
from datetime import datetime
from entrenamiento import Entrenamiento
from workout import es_dia_descanso, rutinas
from spotify import Spotify
import progreso

# ── Paleta Eva-01 ───────────────────────────────────────────
BG          = "#0d0d1a"   # Void
PURPLE      = "#7c3aed"   # Eva purple
LILAC       = "#a78bfa"   # Lilac
LAVENDER    = "#e9d5ff"   # Lavender
GREEN       = "#4ade80"   # Neon green
RED         = "#f87171"   # Alert red
GRAY        = "#8892b0"   # Muted gray
SPOTIFY     = "#1DB954"   # Spotify green
DARK        = "#13131f"   # Abyss

spotify = Spotify()
entrenamiento = Entrenamiento()
entrenamiento.speaker.musica = spotify
hilo = None
ventana_cal = None
ventana_historial = None
ventana_peso = None
ventana_musica = None


def iniciar():
    global hilo
    if hilo and hilo.is_alive():
        return
    hilo = threading.Thread(target=entrenamiento.iniciar, daemon=True)
    hilo.start()


def detener():
    entrenamiento.detener()


def marcar_descanso():
    registrado = progreso.registrar_descanso()
    label_ejercicio.config(
        text="Descanso registrado ✅" if registrado else "Ya registraste el descanso hoy"
    )


# ── Ventanas secundarias ────────────────────────────────────

def abrir_calendario():
    global ventana_cal
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
    ventana_cal.configure(bg=BG)
    ventana_cal.resizable(False, False)

    tk.Label(ventana_cal, text=hoy.strftime("%B %Y"),
             font=("JetBrains Mono", 14, "bold"), fg=LAVENDER, bg=BG
             ).grid(row=0, column=0, columnspan=7, pady=10)

    for col, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
        tk.Label(ventana_cal, text=dia, font=("JetBrains Mono", 9, "bold"),
                 fg=GRAY, bg=BG, width=5).grid(row=1, column=col, padx=2)

    cal = calendar.monthcalendar(anio, mes)
    for fila, semana in enumerate(cal):
        for col, dia in enumerate(semana):
            if dia == 0:
                tk.Label(ventana_cal, text="", bg=BG, width=5).grid(
                    row=fila + 2, column=col, padx=2, pady=2)
                continue
            fecha_str = f"{anio}-{mes:02d}-{dia:02d}"
            if fecha_str == hoy_str:
                color = PURPLE
            elif fecha_str in entrenamientos:
                color = GREEN
            elif fecha_str in descansos:
                color = GRAY
            else:
                color = DARK
            tk.Label(ventana_cal, text=str(dia), font=("JetBrains Mono", 10),
                     fg=LAVENDER, bg=color, width=4, relief="flat",
                     padx=4, pady=4).grid(row=fila + 2, column=col, padx=2, pady=2)

    leyenda = [("● Entrenó", GREEN), ("● Descansó", GRAY), ("● Hoy", PURPLE)]
    for i, (texto, color) in enumerate(leyenda):
        tk.Label(ventana_cal, text=texto, fg=color, bg=BG,
                 font=("JetBrains Mono", 9)).grid(
            row=len(cal) + 3, column=i * 2, columnspan=2, pady=8)


def abrir_historial():
    global ventana_historial
    if ventana_historial and ventana_historial.winfo_exists():
        ventana_historial.lift()
        return
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial semanal")
    ventana_historial.configure(bg=BG)
    ventana_historial.resizable(False, False)
    tk.Label(ventana_historial, text=progreso.resumen_semana_actual(),
             font=("JetBrains Mono", 12), fg=LAVENDER, bg=BG,
             justify="left", padx=20, pady=20).pack()


def abrir_registrar_peso():
    global ventana_peso
    if ventana_peso and ventana_peso.winfo_exists():
        ventana_peso.lift()
        return
    ventana_peso = tk.Toplevel(ventana)
    ventana_peso.title("Registrar peso")
    ventana_peso.configure(bg=BG)
    ventana_peso.resizable(False, False)

    tk.Label(ventana_peso, text="¿Cuánto pesas hoy? (kg)",
             font=("JetBrains Mono", 13, "bold"), fg=LAVENDER, bg=BG).pack(pady=20)
    entrada = tk.Entry(ventana_peso, font=("JetBrains Mono", 20),
                       width=8, justify="center", bg=DARK, fg=LAVENDER,
                       insertbackground=LAVENDER)
    entrada.pack(pady=10)
    entrada.focus()
    label_error = tk.Label(ventana_peso, text="", fg=RED, bg=BG,
                           font=("JetBrains Mono", 10))
    label_error.pack()

    def guardar():
        texto = entrada.get().strip().replace(",", ".")
        try:
            peso = float(texto)
            progreso.registrar_peso(peso)
            ventana_peso.destroy()
            label_ejercicio.config(text=f"Peso registrado: {peso} kg ✅")
        except ValueError:
            label_error.config(text="⚠️ Número inválido")

    tk.Button(ventana_peso, text="GUARDAR", command=guardar,
              width=12, height=2, bg=PURPLE, fg=LAVENDER,
              relief="flat").pack(pady=15)


def abrir_historial_peso():
    global ventana_peso
    if ventana_peso and ventana_peso.winfo_exists():
        ventana_peso.lift()
        return
    ventana_peso = tk.Toplevel(ventana)
    ventana_peso.title("Historial de peso")
    ventana_peso.configure(bg=BG)
    ventana_peso.resizable(False, False)
    tk.Label(ventana_peso, text=progreso.historial_pesos(),
             font=("JetBrains Mono", 12), fg=LAVENDER, bg=BG,
             justify="left", padx=20, pady=20).pack()


def abrir_musica():
    global ventana_musica
    if ventana_musica and ventana_musica.winfo_exists():
        ventana_musica.lift()
        return
    ventana_musica = tk.Toplevel(ventana)
    ventana_musica.title("Spotify")
    ventana_musica.configure(bg=BG)
    ventana_musica.resizable(False, False)
 
    tk.Label(ventana_musica, text="⏺ Spotify",
             font=("JetBrains Mono", 16, "bold"), fg=SPOTIFY, bg=BG).pack(pady=10)
    tk.Label(ventana_musica, text="Link de playlist:",
             font=("JetBrains Mono", 10), fg=GRAY, bg=BG).pack()
    entrada_link = tk.Entry(ventana_musica, font=("JetBrains Mono", 10),
                            width=30, justify="center", bg=DARK,
                            fg=LAVENDER, insertbackground=LAVENDER,
                            relief="flat",
                            bd=0)
    entrada_link.pack(pady=8)

    label_cancion = tk.Label(ventana_musica, text="Sin reproducir",
                             font=("JetBrains Mono", 10), fg=GRAY, bg=BG,
                             wraplength=320)
    label_cancion.pack(pady=5)

    def reproducir():
        link = entrada_link.get().strip()
        if not link:
            label_cancion.config(text="⚠️ Pega un link primero")
            return
        label_cancion.config(text="Cargando...")
        spotify.iniciar_con_link(link)

    tk.Button(ventana_musica, text="▶  REPRODUCIR", command=reproducir,
              width=20, height=2, bg=SPOTIFY, fg="white", relief="flat").pack(pady=10)

    frame_ctrl = tk.Frame(ventana_musica, bg=BG)
    frame_ctrl.pack(pady=5)
    for col, (txt, cmd) in enumerate([("⏮", spotify.anterior),
                                       ("⏯", spotify.play_pause),
                                       ("⏭", spotify.siguiente)]):
        tk.Button(frame_ctrl, text=txt, command=cmd, width=5, height=2,
                  bg=DARK, fg=LAVENDER, relief="flat").grid(
            row=0, column=col, padx=6)

    def actualizar_cancion():
        if spotify.cancion_actual:
            label_cancion.config(text=spotify.cancion_actual, fg=LAVENDER)
        if ventana_musica.winfo_exists():
            ventana_musica.after(2000, actualizar_cancion)

    actualizar_cancion()


def cerrar_app():
    spotify.detener()
    ventana.destroy()


# ── Ventana principal ───────────────────────────────────────

def crear_ventana():
    global ventana, label_ejercicio, label_tiempo, canvas_timer

    ventana = tk.Tk()
    ventana.title("Faper Trainer")
    ventana.geometry("1024x720")
    ventana.configure(bg=BG)
    ventana.resizable(False, False)

    # ── Rutina / nombre ejercicio arriba ────────────────────
    if es_dia_descanso():
        texto_rutina = "💤 Día de Descanso"
        color_rutina = GRAY
    else:
        _, rutina = progreso.rutina_de_hoy(rutinas)
        calorias = rutina["calorias"]
        texto_rutina = f"{rutina['nombre']}  🔥 ~{calorias} kcal"
        color_rutina = LILAC

    label_ejercicio = tk.Label(ventana, text=texto_rutina,
                               font=("JetBrains Mono", 22, "bold"),
                               fg=color_rutina, bg=BG)
    label_ejercicio.pack(pady=(30, 5))

    # ── Fila central: Spotify | Círculo | Iconos ────────────
    frame_medio = tk.Frame(ventana, bg=BG)
    frame_medio.pack(expand=True)

    # Columna izquierda — Spotify
    frame_izq = tk.Frame(frame_medio, bg=BG)
    frame_izq.grid(row=0, column=0, padx=10)

    btn_spotify = tk.Button(frame_izq, text="⏺", font=("JetBrains Mono", 40),
                            fg=SPOTIFY, bg=BG, relief="flat",
                            command=abrir_musica, cursor="hand2")
    btn_spotify.pack()
    label_cancion_mini = tk.Label(frame_izq, text="", font=("JetBrains Mono", 8),
                                  fg=GRAY, bg=BG, wraplength=120, justify="center")
    label_cancion_mini.pack(pady=5)

    # Columna central — Círculo con timer
    RADIO = 200
    canvas_timer = tk.Canvas(frame_medio, width=RADIO * 2, height=RADIO * 2,
                             bg=BG, highlightthickness=0)
    canvas_timer.grid(row=0, column=1, padx=60)

    # Círculo blanco
    canvas_timer.create_oval(4, 4, RADIO * 2 - 4, RADIO * 2 - 4,
                             fill="white", outline=PURPLE, width=3)

    # Timer dentro del círculo
    label_tiempo = tk.Label(canvas_timer, text="0",
                            font=("JetBrains Mono", 110, "bold"),
                            fg=BG, bg="white")
    canvas_timer.create_window(RADIO, RADIO - 30, window=label_tiempo)

    # Botones ▶ ⏸ dentro del círculo
    frame_play = tk.Frame(canvas_timer, bg="white")
    canvas_timer.create_window(RADIO, RADIO + 140, window=frame_play)

    if es_dia_descanso():
        tk.Button(frame_play, text="😴", font=("JetBrains Mono", 20),
                  fg=GRAY, bg="white", relief="flat",
                  command=marcar_descanso).pack(side="left", padx=5)
    else:
        tk.Button(frame_play, text="▶", font=("JetBrains Mono", 20),
                  fg=BG, bg="white", relief="flat",
                  command=iniciar).pack(side="left", padx=5)
        tk.Button(frame_play, text="⏸", font=("JetBrains Mono", 20),
                  fg=RED, bg="white", relief="flat",
                  command=detener).pack(side="left", padx=5)

    # Columna derecha — 4 iconos
    frame_der = tk.Frame(frame_medio, bg=BG)
    frame_der.grid(row=0, column=2, padx=10)

    iconos = [
        ("📅", abrir_calendario,     "Calendario"),
        ("📊", abrir_historial,      "Historial"),
        ("⚖️", abrir_registrar_peso, "Peso"),
        ("📈", abrir_historial_peso, "Ver peso"),
    ]
    for i, (icono, cmd, tooltip) in enumerate(iconos):
        fila = i // 2
        col  = i % 2
        tk.Button(frame_der, text=icono, font=("JetBrains Mono", 28),
                  fg=LAVENDER, bg=BG, relief="flat",
                  command=cmd, cursor="hand2").grid(
            row=fila, column=col, padx=12, pady=12)

    # ── Actualizar labels ───────────────────────────────────
    def actualizar():
        label_ejercicio.config(text=entrenamiento.ejercicio_actual
                               if entrenamiento.activo else texto_rutina)
        label_tiempo.config(text=str(entrenamiento.tiempo_restante)
                            if entrenamiento.activo else "0")
        if spotify.cancion_actual:
            label_cancion_mini.config(text=spotify.cancion_actual)
        ventana.after(200, actualizar)

    actualizar()
    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)
    ventana.mainloop()


if __name__ == "__main__":
    crear_ventana()
