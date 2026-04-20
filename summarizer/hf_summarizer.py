import requests
from dotenv import load_dotenv
from rouge_score import rouge_scorer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {os.environ['HF_API_TOKEN']}",
}

_scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

def summarize_article(title: str, text: str) -> tuple[str, int, int, dict]:

    input_text = f"{title}\n\n{text}"
    original_word_count = len(input_text.split())
    truncated = input_text[:3000]

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": truncated})
    response.raise_for_status()
    result = response.json()

    summary_text: str = result[0]['summary_text']
    summary_word_count = len(summary_text.split())

    scores = _scorer.score(truncated, summary_text)
    rouge_scores = {
        "rouge1": round(scores["rouge1"].fmeasure, 4),
        "rouge2": round(scores["rouge2"].fmeasure, 4),
        "rougeL": round(scores["rougeL"].fmeasure, 4),
    }

    return summary_text, original_word_count, summary_word_count, rouge_scores
