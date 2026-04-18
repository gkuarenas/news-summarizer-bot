# Morning News Summarizer — Telegram Bot

A Python bot that scrapes headlines from **Inquirer, BBC, and TechCrunch**, summarizes them using `facebook/bart-large-cnn` via HuggingFace, and sends a morning digest to Telegram — automatically, every day at 6AM Manila time.

---

## Features

- Scrapes the top 10 latest articles from 3 sources
- Summarizes each article using HuggingFace Inference API
- Sends a formatted digest to a Telegram chat
- Runs daily via GitHub Actions, triggered reliably by cron-job.org

## Tech Stack

| Layer | Tool |
|---|---|
| Scraping | Playwright (Chromium) |
| Summarization | `facebook/bart-large-cnn` (HuggingFace) |
| Delivery | Telegram Bot API |
| Scheduling | GitHub Actions + cron-job.org |

## Project Structure

```
news-summarizer/
├── bot/
├── scrapers/
├── summarizer/
├── .github/workflows/morning-news.yml
└── main.py
```

## Setup

1. Clone the repo and create a virtual environment
2. Install dependencies: `pip install -r requirements.txt && playwright install chromium`
3. Create a `.env` file:

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
HF_API_KEY=
```

4. Run manually: `python main.py`

## Scheduling

Runs daily at **6AM Manila time (UTC+8)** via GitHub Actions `workflow_dispatch`, triggered externally by [cron-job.org](https://cron-job.org) for reliable execution on the free tier.