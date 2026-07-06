# 🏋️ Faper Trainer Minerva
Aplicación de entrenamiento en casa con voz IA para Linux, diseñada para integrarse con tu entorno de escritorio.

## 🔊 Características
- 🔄 Sistema de rutinas rotativas automáticas (Full Body, Tronco Superior, Tronco Inferior)
- ⏱️ Temporizador por intervalos con avisos de voz sincronizados
- 🗣️ Voz IA en español usando Edge TTS (Microsoft Neural)
- 🖥️ GUI con paleta de colores personalizable integrada al entorno
- 📅 Calendario mensual con registro de progreso
- ✅ Registro de días entrenados y días de descanso
- 📊 Historial semanal de entrenamientos
- ⚖️ Registro y seguimiento de peso diario
- 🔥 Calorías aproximadas por rutina
- 😴 Días de descanso automáticos con botón de registro manual
- 🎵 Integración con Spotify vía Brave Browser
- 🔉 Duck de volumen automático cuando habla la IA

## 📋 Requisitos
- Python 3.10+
- ffmpeg
- Brave Browser con sesión de Spotify activa
- picom (recomendado para transparencia de ventana)
- JetBrains Mono (recomendado para la fuente)

## 🚀 Instalación y uso

```bash
git clone https://github.com/lexhoklon/faper-trainer.git
cd faper-trainer
sudo pacman -S ffmpeg ttf-jetbrains-mono    # Arch Linux
pip install edge-tts certifi aiohttp yarl idna playwright --break-system-packages
playwright install chromium
python gui.py
```

## 🎨 Personalización
La app está diseñada para integrarse con entornos bspwm/polybar usando la paleta Eva-01.

### Colores
En `gui.py` puedes cambiar la paleta completa modificando las variables al inicio:
```python
BG      = "#0d0d1a"   # Fondo principal
PURPLE  = "#7c3aed"   # Acento principal
LILAC   = "#a78bfa"   # Acento secundario
LAVENDER= "#e9d5ff"   # Texto principal
GREEN   = "#4ade80"   # Color funcional
RED     = "#f87171"   # Alertas
GRAY    = "#8892b0"   # Texto secundario
```

### Transparencia con picom
Agrega esto a `~/.config/picom/picom.conf`:
    opacity-rule=[
    "90:name='FaperTrainer'"
    ];

Luego reinicia picom:
```bash
pkill picom && picom -b
```

## 🎵 Música con Spotify
Minerva se integra con Spotify a través de Brave Browser — sin APIs de pago, sin configuración extra, usando tu sesión ya iniciada.

> Se eligió Spotify sobre YT Music por su mayor estabilidad, interfaz más predecible y mejor respuesta de los controles de reproducción.

### Uso
1. Haz clic en **⏺** en la app
2. Pega el link de tu playlist de Spotify
3. Presiona **▶ REPRODUCIR**
4. Usa los controles ⏮ ⏯ ⏭ para navegar

La música baja automáticamente de volumen cuando la IA habla y sube al terminar.

### ⚠️ Problemas conocidos
- Al cerrar la app, el proceso de Brave puede quedar corriendo en segundo plano — usar `pkill brave` si es necesario

## ⚙️ Configuración del entrenamiento
Todo se configura desde `workout.py`:

- **Rutinas** — agrega, elimina o modifica los ejercicios de cada rutina
- **Tiempos** — cambia la duración del calentamiento, ejercicios, descansos, recuperación y estiramiento
- **Rondas** — modifica el número de rondas por sesión
- **Calorías** — ajusta las calorías aproximadas de cada rutina
- **Días de descanso** — ajusta qué días de la semana son de descanso

## 📁 Estructura del proyecto
```text
faper-trainer/
├── gui.py           # Interfaz gráfica principal
├── entrenamiento.py # Lógica del entrenamiento y fases
├── workout.py       # Rutinas, ejercicios y tiempos
├── speaker.py       # Motor de voz con Edge TTS
├── progreso.py      # Registro y lectura del progreso
├── spotify.py       # Integración con Spotify
└── progreso.json    # Historial generado automáticamente
```

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
