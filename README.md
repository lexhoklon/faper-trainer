# 🏋️ Faper Trainer
Aplicación de entrenamiento en casa con voz IA para Linux.

## 🔊 Características
- 🔄 Sistema de rutinas rotativas automáticas (Full Body, Tronco Superior, Tronco Inferior)
- ⏱️ Temporizador por intervalos con avisos de voz sincronizados
- 🗣️ Voz IA en español usando Edge TTS (Microsoft Neural)
- 🖥️ GUI simple tipo pantalla de gimnasio
- 📅 Calendario mensual con registro de progreso
- ✅ Registro de días entrenados y días de descanso
- ⏹️ Botón START / STOP

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
- **Días de descanso** — ajusta qué días de la semana son de descanso

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
