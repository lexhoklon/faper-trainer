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
- 🎵 Integración con Spotify y YT Music con controles de reproducción
- 🔉 Duck de volumen automático cuando habla la IA

## 📋 Requisitos
- Python 3.10+
- ffmpeg
- Brave Browser con sesión de Spotify o Google activa

## 🚀 Instalación y uso

```bash
git clone https://github.com/lexhoklon/faper-trainer.git
cd faper-trainer
sudo pacman -S ffmpeg                          # Arch Linux
pip install edge-tts certifi aiohttp yarl idna playwright --break-system-packages
playwright install chromium
python gui.py
```

## 🎵 Música
Soporta Spotify y YT Music a través de Brave Browser con tu sesión ya iniciada.

### Uso
1. Abre la app y haz clic en **🎵 MÚSICA**
2. Selecciona el servicio: **Spotify** o **YT Music**
3. Pega el link de tu playlist
4. Presiona **▶ REPRODUCIR**
5. Usa los controles ⏮ ⏯ ⏭ para navegar

La música baja automáticamente de volumen cuando la IA habla y sube al terminar.

### ⚠️ Problemas conocidos (v5.0)
- La reproducción por link directo de YT Music aún no funciona de forma fiable — se recomienda usar Spotify
- Al cerrar la app, el proceso de Brave puede quedar corriendo en segundo plano — usar `pkill brave` si es necesario

## ⚙️ Configuración
Todo el entrenamiento se configura desde `workout.py`:

- **Rutinas** — agrega, elimina o modifica los ejercicios de cada rutina
- **Tiempos** — cambia la duración del calentamiento, ejercicios, descansos, recuperación y estiramiento
- **Rondas** — modifica el número de rondas por sesión
- **Calorías** — ajusta las calorías aproximadas de cada rutina
- **Días de descanso** — ajusta qué días de la semana son de descanso

## 📁 Estructura del proyecto
|----- gui.py # Interfaz "grafica" principal
|----- entrenamiento.py # Logica del entrenamiento y fases
|----- workout.py # Rutinas, ejercicios y timpos 
|----- speaker.py # Motor de voz con Edge TTS
|----- progreso.py # Registro y lectura del progreso
|----- musica.py # Integración con YT Music
|----- spotify.py # Integración con Spotify
|----- progreso.json # Historial generado automáticamente

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
