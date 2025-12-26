from aiogram import Router, types
from aiogram.filters import CommandStart
from keywords.reply import get_admin_main_menu, get_user_main_menu
from config import ADMINS
from database import Database

router = Router()
db = Database()


@router.message(CommandStart())
async def start_command(message: types.Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id

    # Bazaga yozish
    db.add_user(telegram_id=telegram_id, full_name=full_name)

    if message.from_user.id in ADMINS:
        count = db.count_users()
        await message.answer(
            f"Salom Admin {full_name}!\nBazada {count} ta odam bor.",
            reply_markup=get_admin_main_menu()
        )
    else:
        await message.answer(
            f"Salom {full_name}!",
            reply_markup=get_user_main_menu()
        )