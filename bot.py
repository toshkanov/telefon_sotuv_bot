import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import bot_start # <--- Biz yaratgan handlerni ulaymiz

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(bot_start.router) # <--- Routerni qo'shamiz

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())