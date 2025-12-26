from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database import Database
from config import CHANNEL_URL

db = Database()

# 1. OBUNA TUGMASI
def get_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL))
    builder.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub"))
    builder.adjust(1)
    return builder.as_markup()

# 2. USER MENYUSI (Asosiy)
def get_user_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📱 Telefonlar bozori")
    builder.button(text="➕ E'lon berish")
    builder.button(text="👤 Admin bilan aloqa")
    builder.button(text="📢 Kanalimiz")
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

# 3. KATEGORIYA TANLASH TUGMALARI
def get_categories_buttons():
    builder = ReplyKeyboardBuilder()
    cats = db.get_table_data("categories")
    for cat in cats:
        builder.button(text=cat[1])
    builder.button(text="Bekor qilish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# 4. ADMIN PANEL TUGMALARI (To'liq versiya)
def get_admin_panel_buttons():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Statistika")        # <--- Statistika tugmasi
    builder.button(text="➕ Kategoriya qo'shish") # <--- Kategoriya qo'shish
    builder.button(text="🗄 Bazani ko'rish")
    builder.button(text="Bosh menyuga")         # <--- Orqaga qaytish
    builder.adjust(2, 1, 1)
    return builder.as_markup(resize_keyboard=True)

# Xatolik oldini olish uchun yordamchi
def get_admin_main_menu():
    return get_admin_panel_buttons()