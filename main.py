from scrapers.inquirer import scrape_inquirer, get_article_text_inquirer
from scrapers.bbc import scrape_bbc, get_article_text_bbc
from scrapers.base import close_browser
from summarizer.hf_summarizer import summarize_article
from bot.telegram_bot import send_message
import asyncio
from datetime import date

INQUIRER = 'https://newsinfo.inquirer.net/'
BBC = 'https://www.bbc.com/news/world'

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
    asyncio.run(send_message(header + combined_summaries))

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
    asyncio.run(send_message(header + combined_summaries))

def main():
    today_date = date.today().strftime("%A, %B %d, %Y")
    try:
        inquirer(INQUIRER, today_date)
        bbc(BBC, today_date)
    finally:
        close_browser()

if __name__ == "__main__":
    main()