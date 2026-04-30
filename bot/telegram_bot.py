from dotenv import load_dotenv
import logging
import os
import asyncio
from telegram import Bot

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def send_message(text: str):
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID, 
        text=text,
        parse_mode="MarkdownV2"
    )

if __name__ == '__main__':
    asyncio.run(send_message("Hello!"))