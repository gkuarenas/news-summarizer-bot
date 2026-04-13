# Morning News Summarizer - Telegram Bot

A Python script that scrapes the latest headlines from Inquirer.net (at the moment), summarizes them using the HuggingFace Inference API, and delivers a digest to a Telegram bot every morning.

## Features

- Scrapes the top 10 articles from Inquirer.net
- Summarizes each article using `facebook/bart-large-cnn`
- Sends a formatted digest to a Telegram chat

## Project Structure

```
news-summarizer/
├── bot/
│   └── telegram_bot.py
├── scrapers/
│   └── inquirer.py
│   └── article_parser.py
├── summarizer/
│   └── hf_summarizer.py
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

## Requirements

- Python 3.10+
- Playwright (Chromium)
- HuggingFace Inference API key
- Telegram bot token and chat ID

## Setup

1. Clone the repository.

2. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
playwright install chromium
```

4. Create a `.env` file in the root directory with the following variables.

```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
HF_API_KEY=your_huggingface_api_key_here
```

5. Run the script manually to test.

```bash
python main.py
```

## Notes

- Articles that fail to scrape or summarize are skipped automatically.
