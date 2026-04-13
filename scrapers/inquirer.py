from base import fetch_html, close_browser
from bs4 import BeautifulSoup
import json
import html as html_module
import time

def scrape_inquirer(url):
    soup = fetch_html(url)

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

def get_article_text_inquirer(url: str) -> str:
    soup = fetch_html(url, wait_for="script[type='application/ld+json']")
    script_tag = soup.find("script", type="application/ld+json")

    if script_tag is None:
        raise ValueError(f"No ld+json script tag found on page: {url}")

    data = json.loads(script_tag.string, strict=False)
    article_body_html = html_module.unescape(html_module.unescape(data["articleBody"]))
    body_soup = BeautifulSoup(article_body_html, "html.parser")
    return "\n\n".join(p.get_text() for p in body_soup.find_all("p"))

if __name__ == "__main__":
    test_url = "https://newsinfo.inquirer.net/"
    results = scrape_inquirer(test_url)
    print(len(results))

    time.sleep(2)

    article_url = results[0]["url"]
    print(get_article_text_inquirer(article_url))

    close_browser()

    # fix get_article_tesxt