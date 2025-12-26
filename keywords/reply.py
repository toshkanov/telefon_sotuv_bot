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

# 2. USER MENYUSI (Telefon Bozori)
def get_user_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📱 Telefonlar bozori")
    builder.button(text="➕ E'lon berish")
    builder.button(text="👤 Admin bilan aloqa")
    builder.button(text="📢 Kanalimiz")
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

# 3. KATEGORIYALAR
def get_categories_buttons():
    builder = ReplyKeyboardBuilder()
    cats = db.get_table_data("categories")
    for cat in cats:
        builder.button(text=cat[1])
    builder.button(text="Bekor qilish")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# 4. ADMIN PANEL
def get_admin_panel_buttons():
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Kategoriya qo'shish")
    builder.button(text="🗄 Bazani ko'rish")
    builder.button(text="Bosh menyuga")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

# --- QO'SHIMCHA (Xatolikni yo'qotish uchun) ---
def get_admin_main_menu():
    # Eski kodlar xato bermasligi uchun Admin Panelni qaytaradi
    return get_admin_panel_buttons()