import requests
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.article_parser import get_article_text

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {os.environ['HF_API_TOKEN']}",
}

def summarize_article(title, url):
    text = get_article_text(url)

    input_text = f"{title}\n\n{text}"
    input_text = input_text[:3000]

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": input_text})
    result = response.json()

    return result[0]["summary_text"]

if __name__ == '__main__':
    test_title = "Diesel to drop by nearly P21/L as gasoline prices also cut"
    test_url = "https://newsinfo.inquirer.net/2211062/diesel-to-drop-by-nearly-p21-l-as-gasoline-prices-also-cut"
    print(summarize_article(test_title, test_url))