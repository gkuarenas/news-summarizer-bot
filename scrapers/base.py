from playwright.sync_api import sync_playwright, Browser
from bs4 import BeautifulSoup

_playwright = None
_browser = None

def get_browser() -> Browser:
    global _playwright, _browser
    if _browser is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
    return _browser

def fetch_html(url: str, wait_for: str = None) -> BeautifulSoup:
    browser = get_browser()
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
    )
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    if wait_for:
        page.wait_for_selector(wait_for, state='attached', timeout=10000)
    html = page.content()
    context.close()
    return BeautifulSoup(html, "html.parser")

def close_browser():
    global _playwright, _browser
    if _browser:
        _browser.close()
        _playwright.stop()
        _browser = None
        _playwright = None