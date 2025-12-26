from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from config import ADMINS, CHANNEL_ID
from keywords.reply import get_user_main_menu, get_admin_panel_buttons, get_subscription_keyboard
from database import Database

router = Router()
db = Database()

async def check_user_subscription(user_id, bot: Bot):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except:
        return False

@router.message(CommandStart())
async def start_command(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.full_name)

    if await check_user_subscription(user_id, bot):
        if str(user_id) in ADMINS:
            await message.answer("Salom Admin!", reply_markup=get_admin_panel_buttons())
        else:
            await message.answer("Xush kelibsiz!", reply_markup=get_user_main_menu())
    else:
        await message.answer("Botdan foydalanish uchun kanalga a'zo bo'ling:", reply_markup=get_subscription_keyboard())

@router.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: CallbackQuery, bot: Bot):
    if await check_user_subscription(callback.from_user.id, bot):
        await callback.message.delete()
        await callback.message.answer("Obuna tasdiqlandi! ✅", reply_markup=get_user_main_menu())
    else:
        await callback.answer("Hali obuna bo'lmadingiz!", show_alert=True)