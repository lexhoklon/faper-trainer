import threading
import tkinter as tk
from entrenamiento import Entrenamiento

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

    ventana.after(200, actualizar_labels)  # refresca cada 200ms


def crear_ventana():
    global ventana, label_ejercicio, label_tiempo

    ventana = tk.Tk()
    ventana.title("Faper Trainer")
    ventana.geometry("800x600")
    ventana.configure(bg="black")

    # 🔥 nombre ejercicio (GRANDE)
    label_ejercicio = tk.Label(
        ventana,
        text="Listo",
        font=("Arial", 40, "bold"),
        fg="white",
        bg="black"
    )
    label_ejercicio.pack(pady=40)

    # ⏱ tiempo (MUY GRANDE)
    label_tiempo = tk.Label(
        ventana,
        text="0",
        font=("Arial", 80, "bold"),
        fg="green",
        bg="black"
    )
    label_tiempo.pack(pady=20)

    # botones
    tk.Button(ventana, text="START", command=iniciar, width=20, height=2).pack(pady=10)
    tk.Button(ventana, text="STOP", command=detener, width=20, height=2).pack(pady=10)

    actualizar_labels()

    ventana.mainloop()


if __name__ == "__main__":
    crear_ventana()
