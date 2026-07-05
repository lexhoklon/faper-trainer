import time
import asyncio
from spotify import Spotify

s = Spotify()
s.iniciar_con_link("https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP")

print("Esperando que cargue...")
time.sleep(20)
print(f"Sonando: {s.cancion_actual}")

async def check_audio():
    info = await s._page.evaluate("""
        () => {
            // Buscamos el slider de volumen de Spotify
            const slider = document.querySelector('[data-testid="volume-bar"]');
            const sliderInput = document.querySelector('[data-testid="volume-bar-toggle"]');
            const allSliders = document.querySelectorAll('input[type="range"]');
            
            return {
                tiene_slider: !!slider,
                tiene_slider_input: !!sliderInput,
                sliders: Array.from(allSliders).map(s => ({
                    label: s.getAttribute('aria-label'),
                    value: s.value,
                    min: s.min,
                    max: s.max
                }))
            }
        }
    """)
    print(f"Audio info: {info}")

print("Chequeando audio...")
asyncio.run_coroutine_threadsafe(check_audio(), s._loop).result()

print("Bajando volumen...")
s.bajar_volumen()
time.sleep(4)

asyncio.run_coroutine_threadsafe(check_audio(), s._loop).result()
