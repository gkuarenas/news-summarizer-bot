from scrapers.inquirer import scrape_inquirer
from summarizer.hf_summarizer import summarize_article
from bot.telegram_bot import send_message
import asyncio
from datetime import date

def main():
    articles = scrape_inquirer()[:10]
    summary_list = []

    for a in articles:
        title = a.get("title")
        url = a.get("url")

        try:
            summary = summarize_article(title, url)
            print(f"Summarizing: {title}...")
            summary_list.append(summary)
        except Exception:
            continue
    
    today = date.today().strftime("%A, %B %d, %Y")
    header = f'----- INQUIRER LATEST NEWS ({today}) ----- \n\n'
    combined_summaries = "\n\n".join(summary_list)
    asyncio.run(send_message(header + combined_summaries))
    

if __name__ == "__main__":
    main()