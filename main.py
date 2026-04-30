from scrapers.inquirer import scrape_inquirer, get_article_text_inquirer
from scrapers.bbc import scrape_bbc, get_article_text_bbc
from scrapers.techcrunch import scrape_techcrunch, get_article_text_techcrunch
from scrapers.base import close_browser
from summarizer.hf_summarizer import summarize_article
from bot.telegram_bot import send_message
from bot.formatter import format_section
from run_metrics import RunMetrics
from datetime import datetime, timezone, timedelta
import asyncio

INQUIRER = 'https://newsinfo.inquirer.net/'
BBC = 'https://www.bbc.com/news/world'
TECHCRUNCH = "https://techcrunch.com/"


async def _summarize_articles(articles: list[dict], get_text_fn, metrics: RunMetrics) -> list[str]:
    summary_list = []

    for a in articles:
        title = a.get("title")
        article_url = a.get("url")
        metrics.record_article_attempt()
        try:
            text = await get_text_fn(article_url)
            summary_text, original_words, summary_words, rouge_scores = summarize_article(title, text)
            print(f"Summarizing: {title} {article_url}")
            metrics.record_article_success(original_words, summary_words, rouge_scores)

            compression = round((1 - summary_words / original_words) * 100, 2)
            print(f"  → compressed by {compression}%  |  ROUGE-L {rouge_scores['rougeL']}")

            summary_list.append({"title": title,
                                 "url": article_url,
                                 "summary": summary_text})
        except Exception as e:
            print(f"Skipping article '{title}': {e}")

    return summary_list


async def inquirer(url: str, today: str, metrics: RunMetrics):
    articles = await scrape_inquirer(url)
    articles = articles[:5]
    summary_list = await _summarize_articles(articles, get_article_text_inquirer, metrics)
    message = format_section(f"🇵🇭 PH News (Inquirer) - {today}", summary_list)
    print(message)
    await send_message(message)


async def bbc(url: str, today: str, metrics: RunMetrics):
    articles = await scrape_bbc(url)
    articles = articles[:5]
    summary_list = await _summarize_articles(articles, get_article_text_bbc, metrics)
    await send_message(format_section(f"🌍 World News (BBC) - {today}", summary_list))
    


async def techcrunch(url: str, today: str, metrics: RunMetrics):
    articles = await scrape_techcrunch(url)
    articles = articles[:5]
    summary_list = await _summarize_articles(articles, get_article_text_techcrunch, metrics)
    await send_message(format_section(f"💻 Tech (TechCrunch) - {today}", summary_list))


async def main():
    manila_tz = timezone(timedelta(hours=8))
    today_date = datetime.now(manila_tz).strftime("%B %d, %Y")

    metrics = RunMetrics()

    scrapers = [
        (inquirer,   INQUIRER),
        (bbc,        BBC),
        (techcrunch, TECHCRUNCH),
    ]

    for scraper_fn, url in scrapers:
        name = scraper_fn.__name__
        try:
            await scraper_fn(url, today_date, metrics)
            metrics.record_scraper_success()
        except Exception as e:
            print(f"[ERROR] {name} failed: {e}")
            metrics.record_scraper_failure(name)

    await close_browser()
    metrics.flush()


if __name__ == "__main__":
    asyncio.run(main())  # single event loop, owns everything