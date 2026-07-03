import asyncio

async def debug():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        url = "https://music.youtube.com/search?q=workout+playlist"
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        await page.screenshot(path="debug.png")

        # Buscamos todos los botones con aria-label que contengan "play" o "reproducir"
        botones = await page.evaluate("""
            () => {
                const elements = document.querySelectorAll('[aria-label]');
                return Array.from(elements)
                    .map(el => ({
                        tag: el.tagName,
                        label: el.getAttribute('aria-label'),
                        parent: el.parentElement ? el.parentElement.tagName : ''
                    }))
                    .filter(el => 
                        el.label && (
                            el.label.toLowerCase().includes('play') ||
                            el.label.toLowerCase().includes('repro') ||
                            el.label.toLowerCase().includes('aleatorio')
                        )
                    );
            }
        """)
        
        print("Botones encontrados:")
        for b in botones:
            print(f"  {b['tag']} | label: {b['label']} | padre: {b['parent']}")

asyncio.run(debug())
