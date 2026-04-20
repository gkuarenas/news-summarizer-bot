import requests
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {os.environ['HF_API_TOKEN']}",
}

def summarize_article(title, text):

    input_text = f"{title}\n\n{text}"
    original_word_count = len(input_text.split())
    input_text = input_text[:3000]

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": input_text})
    result = response.json()

    summary_word_count = len(result[0]["summary_text"].split())

    return result[0]["summary_text"], original_word_count, summary_word_count
