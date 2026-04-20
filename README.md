# Morning News Summarizer — Telegram Bot

A Python bot that scrapes headlines from **Inquirer, BBC, and TechCrunch**, summarizes them using `facebook/bart-large-cnn` via HuggingFace, and sends a morning digest to Telegram — automatically, every day at 6AM Manila time.

---

## Features

- Scrapes the top 10 latest articles from 3 sources
- Summarizes each article using HuggingFace Inference API
- Sends a formatted digest to a Telegram chat
- Runs daily via GitHub Actions, triggered reliably by cron-job.org
- Logs per-run metrics to `metrics.csv` (committed back to the repo automatically)
- Posts a metrics summary to the GitHub Actions Job Summary after each run

## Tech Stack

| Layer | Tool |
|---|---|
| Scraping | Playwright (Chromium) |
| Summarization | `facebook/bart-large-cnn` (HuggingFace) |
| Delivery | Telegram Bot API |
| Scheduling | GitHub Actions + cron-job.org |
| Metrics | `rouge-score`, `metrics.csv`, GitHub Actions Job Summary |

## Project Structure

```
news-summarizer/
├── bot/
├── scrapers/
├── summarizer/
├── .github/workflows/summarizer.yml
├── run_metrics.py
├── metrics.csv
└── main.py
```

## Setup

1. Clone the repo and create a virtual environment
2. Install dependencies: `pip install -r requirements.txt && playwright install chromium`
3. Create a `.env` file:

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
HF_API_TOKEN=
```

4. Run manually: `python main.py`

## Scheduling

Runs daily at **6AM Manila time (UTC+8)** via GitHub Actions `workflow_dispatch`, triggered externally by [cron-job.org](https://cron-job.org) for reliable execution on the free tier.

## Metrics Logging

Each run appends a row to `metrics.csv` and posts a summary table to the GitHub Actions Job Summary.

### metrics.csv columns

| Column | Description |
|---|---|
| `run_date` | ISO-8601 UTC timestamp of the run |
| `status` | `SUCCESS` or `FAILED` |
| `scrapers_ok` | Number of scrapers that completed successfully |
| `scrapers_failed` | Number of scrapers that failed |
| `articles_scraped` | Total articles attempted across all sources |
| `articles_ok` | Articles successfully summarized |
| `avg_compression` | Mean compression ratio across all articles (%) |
| `avg_rouge1` | Mean ROUGE-1 F1 score |
| `avg_rouge2` | Mean ROUGE-2 F1 score |
| `avg_rougeL` | Mean ROUGE-L F1 score |

### How it works

- `run_metrics.py` defines a `RunMetrics` class that accumulates stats during the run
- At the end of `main.py`, `metrics.flush()` writes the CSV row and the Job Summary
- The GitHub Actions workflow commits `metrics.csv` back to the repo with `[skip ci]` to avoid triggering another run
- ROUGE scores are computed locally via `rouge-score` against the truncated input, measuring how much of the source content the summary covers
