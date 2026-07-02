# 🏋️ Faper Trainer
Aplicación de entrenamiento en casa con voz IA para Linux.

## 🔊 Características
- 🔄 Sistema de rutinas rotativas automáticas (Full Body, Tronco Superior, Tronco Inferior)
- ⏱️ Temporizador por intervalos con avisos de voz sincronizados
- 🗣️ Voz IA en español usando Edge TTS (Microsoft Neural)
- 🖥️ GUI centrada tipo pantalla de gimnasio
- 📅 Calendario mensual con registro de progreso
- ✅ Registro de días entrenados y días de descanso
- 📊 Historial semanal de entrenamientos
- ⚖️ Registro y seguimiento de peso diario
- 🔥 Calorías aproximadas por rutina
- 😴 Días de descanso automáticos con botón de registro manual

## 📋 Requisitos
- Python 3.10+
- ffmpeg

## 🚀 Instalación y uso

```bash
git clone https://github.com/lexhoklon/faper-trainer.git
cd faper-trainer
sudo pacman -S ffmpeg        # Arch Linux
pip install edge-tts certifi aiohttp yarl idna --break-system-packages
python gui.py
```

## ⚙️ Configuración
Todo el entrenamiento se configura desde `workout.py`:

- **Rutinas** — agrega, elimina o modifica los ejercicios de cada rutina
- **Tiempos** — cambia la duración del calentamiento, ejercicios, descansos, recuperación y estiramiento
- **Rondas** — modifica el número de rondas por sesión
- **Calorías** — ajusta las calorías aproximadas de cada rutina
- **Días de descanso** — ajusta qué días de la semana son de descanso

## 📁 Estructura del proyecto
faper-trainer/
├── gui.py # Interfaz gráfica principal
├── entrenamiento.py # Lógica del entrenamiento y fases
├── workout.py # Rutinas, ejercicios y tiempos
├── speaker.py # Motor de voz con Edge TTS
├── progreso.py # Registro y lectura del progreso
└── progreso.json # Historial generado automáticamente

## 🗣️ Cambiar la voz
En `speaker.py` puedes cambiar la variable `VOZ`:
```python
VOZ = "es-ES-AlvaroNeural"   # España (hombre)
VOZ = "es-ES-ElviraNeural"   # España (mujer)
VOZ = "es-MX-JorgeNeural"    # México (hombre)
VOZ = "es-MX-DaliaNeural"    # México (mujer)
```
Para ver todas las voces disponibles:
```bash
edge-tts --list-voices | grep es-
```
