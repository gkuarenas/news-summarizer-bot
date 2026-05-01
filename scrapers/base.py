from playwright.async_api import async_playwright, Browser
from bs4 import BeautifulSoup
import asyncio
import random


async def fetch_html(url: str, wait_for: str = None, retries: int = 3) -> BeautifulSoup:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )

        for attempt in range(retries):
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                }
            )
            try:
                page = await context.new_page()
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                if wait_for:
                    await page.wait_for_selector(wait_for, state="attached", timeout=10000)
                    await page.wait_for_timeout(2000)

                html = await page.content()
                await context.close()

                await asyncio.sleep(random.uniform(1.5, 3.5))

                await browser.close()
                return BeautifulSoup(html, "html.parser")

            except Exception as e:
                await context.close()
                if attempt < retries - 1:
                    wait = 2 ** attempt + random.uniform(1, 3)
                    print(f"Attempt {attempt + 1} failed for {url}: {e}. Retrying in {wait:.1f}s...")
                    await asyncio.sleep(wait)
                else:
                    await browser.close()
                    raise


async def close_browser():
    pass
