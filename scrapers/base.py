from playwright.sync_api import sync_playwright, Browser
from bs4 import BeautifulSoup
import time
import random

_playwright = None
_browser = None

def get_browser() -> Browser:
    global _playwright, _browser
    if _browser is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
    return _browser

def fetch_html(url: str, wait_for: str = None, retries: int = 3) -> BeautifulSoup:
    browser = get_browser()

    for attempt in range(retries):
        context = browser.new_context(
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
            page = context.new_page()

            # Hide webdriver property
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            if wait_for:
                page.wait_for_selector(wait_for, state="attached", timeout=10000)

            html = page.content()
            context.close()

            # Random delay between requests to avoid rate limiting
            time.sleep(random.uniform(1.5, 3.5))

            return BeautifulSoup(html, "html.parser")

        except Exception as e:
            context.close()
            if attempt < retries - 1:
                wait = 2 ** attempt + random.uniform(1, 3)
                print(f"Attempt {attempt + 1} failed for {url}: {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
            else:
                raise

def close_browser():
    global _playwright, _browser
    if _browser:
        _browser.close()
        _playwright.stop()
        _browser = None
        _playwright = None