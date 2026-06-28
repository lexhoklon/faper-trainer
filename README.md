# 🏋️ Faper Trainer
Aplicación de entrenamiento con voz para Linux.

## 🔊 Características
- Entrenamiento por rondas configurable
- Temporizador con cuenta regresiva
- Voz IA en español usando Edge TTS (Microsoft Neural)
- GUI simple tipo pantalla de gimnasio
- Botón START / STOP

## Requisitos
- Python 3.10+
- ffmpeg instalado

## 🚀 Instalación y uso

```bash
git clone https://github.com/lexhoklon/faper-trainer.git
cd faper-trainer
pip install edge-tts
python gui.py
```

## ⚙️ Configurar el entrenamiento
Edita `workout.py` para cambiar ejercicios, tiempos y rondas.

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
