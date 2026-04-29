from scrapers.base import fetch_html, close_browser
import time

async def scrape_bbc(url):
    soup = await fetch_html(url)

    articles = []
    h2_tags = soup.find_all("h2", attrs={'data-testid': 'card-headline'})
    for h2 in h2_tags:
        title = h2.get_text()
        a_tag = h2.find_parent("a")
        href = "https://www.bbc.com" + a_tag["href"]
        
        if title and href:
            articles.append({"title": title, "url": href})
    
    return articles

async def get_article_text_bbc(url: str) -> str:
    soup = await fetch_html(url)
    paragraphs = soup.find_all("p")
    return "\n\n".join(p.get_text() for p in paragraphs)

if __name__ == '__main__':
    test_url = "https://www.bbc.com/news/world"
    results = scrape_bbc(test_url)
    print(len(results))

    time.sleep(2)

    article_url = results[0]["url"]
    print(get_article_text_bbc(article_url))

    close_browser()
