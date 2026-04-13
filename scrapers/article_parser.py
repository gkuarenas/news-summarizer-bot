import json
import html as html_module
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_article_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    data = json.loads(script_tag.string, strict=False)
    article_body_html = html_module.unescape(html_module.unescape(data["articleBody"]))

    body_soup = BeautifulSoup(article_body_html, "html.parser")
    paragraphs = body_soup.find_all("p")
    full_text = "\n\n".join(p.get_text() for p in paragraphs)
    return full_text


if __name__ == "__main__":
    test_url = "https://newsinfo.inquirer.net/2211062/diesel-to-drop-by-nearly-p21-l-as-gasoline-prices-also-cut"
    print(get_article_text(test_url))