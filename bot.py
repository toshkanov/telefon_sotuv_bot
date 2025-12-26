import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Handlers
from handlers import bot_start, admin, user_menu, echo
from config import TOKEN

load_dotenv()
dp = Dispatcher()

# ... (tepadagi importlar) ...

# Routerlarni ulash tartibi:
dp.include_router(admin.router)      # 1. Admin
dp.include_router(bot_start.router)  # 2. Start va Obuna
dp.include_router(user_menu.router)  # 3. E'lon berish va Savdo
# dp.include_router(echo.router)     # 4. (Ixtiyoriy)

# ...
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())