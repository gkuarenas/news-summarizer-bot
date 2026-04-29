from scrapers.base import fetch_html, close_browser
import time

async def scrape_techcrunch(url):
    soup = await fetch_html(url)

    articles = []

    article = soup.find_all("a", class_="loop-card__title-link")

    for a in article:
        title = a.text
        href = a.get('href')

        if title and href:
            articles.append({"title": title, "url": href})
    
    return articles


async def get_article_text_techcrunch(url: str) -> str:
    soup = await fetch_html(url)
    paragraphs = soup.find_all("p", class_='wp-block-paragraph')
    return "\n\n".join(p.get_text() for p in paragraphs)


if __name__ == "__main__":
    test_url = "https://techcrunch.com/category/artificial-intelligence/"
    results = scrape_techcrunch(test_url)
    print(len(results))

    time.sleep(2)

    article_url = results[0]["url"]
    print(article_url)
    print(get_article_text_techcrunch(article_url))

    close_browser()