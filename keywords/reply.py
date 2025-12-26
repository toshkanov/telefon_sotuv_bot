from aiogram.utils.keyboard import ReplyKeyboardBuilder

COURSES = ["AI kursi", "Backend", "Frontend", "Flutter", "Mobil dasturlash", "3Ds Max"]

def get_admin_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Admin Panel")
    builder.button(text="Kurslar haqida ma'lumot")
    builder.button(text="Manzilimiz")
    builder.button(text="Bot haqida")
    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_user_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Kurslar haqida ma'lumot")
    builder.button(text="Manzilimiz")
    builder.button(text="Bot haqida")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_courses_menu():
    builder = ReplyKeyboardBuilder()
    for course in COURSES:
        builder.button(text=course)
    builder.button(text="Bosh menyuga")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_course_inner_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Ro'yxatdan o'tish")
    builder.button(text="Orqaga qaytish")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_bot_bio():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Bosh menyuga")
    return builder.as_markup(resize_keyboard=True)


# Admin Panel ichidagi tugmalar
def get_admin_panel_buttons():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Statistika")
    builder.button(text="📢 Reklama yuborish")
    builder.button(text="Bosh menyuga")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)