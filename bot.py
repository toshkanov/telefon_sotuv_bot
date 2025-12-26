import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Handlers
from handlers import bot_start, admin, user_menu, echo
from config import TOKEN

load_dotenv()
dp = Dispatcher()

# Routerlarni ulash tartibi MUHIM!
dp.include_router(admin.router)      # 1. Admin buyruqlari
dp.include_router(bot_start.router)  # 2. Start
dp.include_router(user_menu.router)  # 3. User menyulari (Kurslar, Manzil)
dp.include_router(echo.router)       # 4. Eng oxirida (boshqa narsaga tushmasa)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())