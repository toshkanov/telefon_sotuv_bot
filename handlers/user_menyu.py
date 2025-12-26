from aiogram import Router, F, types
from keywords.reply import get_courses_menu, get_course_inner_menu, get_bot_bio, get_admin_main_menu, get_user_main_menu, COURSES
from config import ADMINS

router = Router()

@router.message(F.text == "Manzilimiz")
async def show_address(message: types.Message):
    await message.answer("Qashqadaryo viloyati, Kitob tumani, Rezvon svetofori oldida")

@router.message(F.text == "Kurslar haqida ma'lumot")
async def show_courses(message: types.Message):
    await message.answer("Bizning mavjud kurslarimiz ro'yxati:", reply_markup=get_courses_menu())

@router.message(F.text.in_(COURSES))
async def show_course_details(message: types.Message):
    await message.answer(f"Siz {message.text} kursini tanladingiz.", reply_markup=get_course_inner_menu())

@router.message(F.text == "Ro'yxatdan o'tish")
async def register_action(message: types.Message):
    await message.answer("Tez orada operatorlarimiz bog'lanadi")

@router.message(F.text == "Orqaga qaytish")
async def back_to_courses(message: types.Message):
    await message.answer("Kurslar ro'yxati:", reply_markup=get_courses_menu())

@router.message(F.text == "Bosh menyuga")
async def back_main(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Bosh menyu (Admin):", reply_markup=get_admin_main_menu())
    else:
        await message.answer("Bosh menyu:", reply_markup=get_user_main_menu())

@router.message(F.text == "Bot haqida")
async def show_bot_bio(message: types.Message):
    await message.answer("Bot haqida ma'lumot...", reply_markup=get_bot_bio())