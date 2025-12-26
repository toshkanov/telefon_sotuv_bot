from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_admin_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Admin Panel")
    builder.button(text="Statistika")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_user_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Kurslar")
    builder.button(text="Biz haqimizda")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)