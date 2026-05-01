from scrapers.base import fetch_html, close_browser
from bs4 import BeautifulSoup
import json
import html as html_module
import asyncio

async def scrape_inquirer(url):
    soup = await fetch_html(url)

    articles = []

    featured = soup.find_all("div", id="cmr-info")
    rest = soup.find_all("div", id="ncg-info")
    featured_links = [a for div in featured for a in div.find_all("a")]
    rest_links = [a for div in rest for a in div.find_all("a")]
    links = featured_links + rest_links

    for link in links:
        title = link.text
        href = link.get("href")

        if title and href:
            articles.append({"title": title, "url": href})
            
    return articles

async def get_article_text_inquirer(url: str) -> str:
    soup = await fetch_html(url)
    
    # Target the article body container directly
    article = soup.find("div", class_="article-content-body")
    if article:
        paragraphs = article.find_all("p")
        if paragraphs:
            print("[debug] using DOM scrape path")
            return "\n\n".join(p.get_text() for p in paragraphs)
    
    # Fallback: ld+json
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag and script_tag.string:
        data = json.loads(script_tag.string, strict=False)
        if "articleBody" in data:
            article_body_html = html_module.unescape(html_module.unescape(data["articleBody"]))
            body_soup = BeautifulSoup(article_body_html, "html.parser")
            paragraphs = body_soup.find_all("p")
            if paragraphs:
                return "\n\n".join(p.get_text() for p in paragraphs)
            print("[debug] using ld+json path")
            return body_soup.get_text()
    
    raise ValueError(f"Could not extract article body from {url}")

if __name__ == "__main__":
    async def _test():
        test_url = "https://newsinfo.inquirer.net/"
        results = await scrape_inquirer(test_url)
        print(len(results))
        article_url = results[0]["url"]
        print(await get_article_text_inquirer(article_url))
        await close_browser()

    asyncio.run(_test())