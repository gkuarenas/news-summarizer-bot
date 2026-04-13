from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_bbc():
    url = "https://www.bbc.com/news/world"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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

    articles = []
    h2_tags = soup.find_all("h2", attrs={'data-testid': 'card-headline'})
    for h2 in h2_tags:
        title = h2.get_text()
        a_tag = h2.find_parent("a")
        href = "https://www.bbc.com" + a_tag["href"]
        
        if title and href:
            articles.append({"title": title, "url": href})
    
    return articles

if __name__ == '__main__':
    results = scrape_bbc()
    for r in results:
        print(r)
    
    print(len(results))
