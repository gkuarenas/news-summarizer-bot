from scrapers.inquirer import scrape_inquirer, get_article_text_inquirer
from scrapers.bbc import scrape_bbc, get_article_text_bbc
from scrapers.base import close_browser
from summarizer.hf_summarizer import summarize_article
from bot.telegram_bot import send_message
from datetime import date
import asyncio
import concurrent.futures

INQUIRER = 'https://newsinfo.inquirer.net/'
BBC = 'https://www.bbc.com/news/world'

def send(text: str):
    """Safely run the async send_message from a synchronous context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Playwright may leave a running loop — spin up a fresh thread with its own loop
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, send_message(text))
                future.result()
        else:
            loop.run_until_complete(send_message(text))
    except RuntimeError:
        asyncio.run(send_message(text))

def inquirer(url: str, today: str):
    articles = scrape_inquirer(url)[:10]
    summary_list = []

    for a in articles:
        title = a.get("title")
        article_url = a.get("url")
        try:
            text = get_article_text_inquirer(article_url)
            summary = summarize_article(title, text)
            print(f"Summarizing: {title}...")
            summary_list.append(summary)
        except Exception as e:
            print(f"Skipping article '{title}': {e}")
            continue

    header = f'----- INQUIRER LATEST NEWS ({today}) ----- \n\n'
    combined_summaries = "\n\n".join(summary_list)
    send(header + combined_summaries)

def bbc(url: str, today: str):
    articles = scrape_bbc(url)[:10]
    summary_list = []

    for a in articles:
        title = a.get("title")
        article_url = a.get("url")
        try:
            text = get_article_text_bbc(article_url)
            summary = summarize_article(title, text)
            print(f"Summarizing: {title}...")
            summary_list.append(summary)
        except Exception as e:
            print(f"Skipping article '{title}': {e}")
            continue

    header = f'----- BBC LATEST NEWS ({today}) ----- \n\n'
    combined_summaries = "\n\n".join(summary_list)
    send(header + combined_summaries)

def main():
    today_date = date.today().strftime("%A, %B %d, %Y")
    try:
        inquirer(INQUIRER, today_date)
        bbc(BBC, today_date)
    finally:
        close_browser()

if __name__ == "__main__":
    main()