from aiogram import Router, F, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart

router = Router()

# 1. Guruhda /start bosilsa
@router.message(CommandStart(), F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def group_start_handler(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}! Men guruhlarda ham ishlayman. Shaxsiyga o'tib yozishingiz mumkin.")

# 2. Guruhga yangi odam qo'shilsa (Kutib olish)
@router.message(F.new_chat_members)
async def new_member_handler(message: types.Message):
    for user in message.new_chat_members:
        # Agar botning o'zi qo'shilsa
        if user.id == message.bot.id:
            await message.answer("Guruhga qo'shganingiz uchun rahmat!")
        else:
            await message.answer(f"Xush kelibsiz, {user.full_name}!")