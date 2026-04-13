import requests
from bs4 import BeautifulSoup

def scrape_inquirer():
    url = "https://newsinfo.inquirer.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

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

if __name__ == "__main__":
    results = scrape_inquirer()
    for r in results:
        print(r)

    print(len(results))