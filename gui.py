import threading
import tkinter as tk
import calendar
from datetime import datetime
from entrenamiento import Entrenamiento
from workout import es_dia_descanso, rutinas
import progreso

entrenamiento = Entrenamiento()
hilo = None


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


def crear_ventana():
    global ventana, label_ejercicio, label_tiempo

    ventana = tk.Tk()
    ventana.title("Faper Trainer")
    ventana.geometry("800x600")
    ventana.configure(bg="black")

    if es_dia_descanso():
        texto_rutina = "💤 Día de Descanso"
        color_rutina = "gray"
    else:
        _, rutina = progreso.rutina_de_hoy(rutinas)
        texto_rutina = f"Rutina de hoy: {rutina['nombre']}"
        color_rutina = "yellow"

    tk.Label(
        ventana,
        text=texto_rutina,
        font=("Arial", 24, "bold"),
        fg=color_rutina,
        bg="black"
    ).pack(pady=20)

    label_ejercicio = tk.Label(
        ventana,
        text="Listo",
        font=("Arial", 40, "bold"),
        fg="white",
        bg="black"
    )
    label_ejercicio.pack(pady=20)

    label_tiempo = tk.Label(
        ventana,
        text="0",
        font=("Arial", 80, "bold"),
        fg="green",
        bg="black"
    )
    label_tiempo.pack(pady=20)

    estado_boton = "disabled" if es_dia_descanso() else "normal"

    tk.Button(ventana, text="START", command=iniciar,
              width=20, height=2, state=estado_boton).pack(pady=10)

    tk.Button(ventana, text="STOP", command=detener,
              width=20, height=2).pack(pady=10)

    tk.Button(ventana, text="📅 VER PROGRESO", command=abrir_calendario,
              width=20, height=2, bg="#1a1a2e", fg="white").pack(pady=10)

    if es_dia_descanso():
        tk.Button(ventana, text="MARCAR DESCANSO ✅", command=marcar_descanso,
                  width=20, height=2, bg="gray", fg="white").pack(pady=10)

    actualizar_labels()
    ventana.mainloop()


if __name__ == "__main__":
    crear_ventana()
