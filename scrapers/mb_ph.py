import requests
from bs4 import BeautifulSoup

def scrape_manila_bulletin():
    url = "https://newsinfo.inquirer.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    links = soup.find_all("a", class_="relative")

    for link in links:
        title = link.get("title")
        href = link.get("href")

        if title and href:
            articles.append({"title": title, "url": href})
            
    return articles

if __name__ == "__main__":
    results = scrape_manila_bulletin()
    for r in results:
        print(r)

    print(len(results))