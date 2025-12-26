from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMINS
from keywords.reply import get_admin_panel_buttons, get_user_main_menu
from database import Database

router = Router()
db = Database()


# Holatlar (States)
class AdminState(StatesGroup):
    waiting_for_category_name = State()


# --- 1. ADMIN PANELGA KIRISH ---
@router.message(F.text == "Admin Panel")
async def admin_panel(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Admin Panelga xush kelibsiz! 👨‍💻", reply_markup=get_admin_panel_buttons())


# --- 2. STATISTIKA (YANGI va KUCHAYTIRILGAN) ---
@router.message(F.text == "📊 Statistika")
async def show_full_stats(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        # Bazadan ma'lumotlarni olamiz
        stats = db.get_full_statistics()

        # 1. Umumiy hisobot
        text = (f"📊 <b>LOYIHA STATISTIKASI</b>\n"
                f"➖➖➖➖➖➖➖➖➖➖\n"
                f"👥 <b>Jami foydalanuvchilar:</b> {stats['users_count']} ta\n"
                f"📱 <b>Jami e'lonlar:</b> {stats['products_count']} ta\n"
                f"➖➖➖➖➖➖➖➖➖➖\n\n")

        # 2. Kategoriyalar bo'yicha
        text += "📂 <b>Kategoriyalar bo'yicha:</b>\n"
        if stats['categories']:
            for cat_name, count in stats['categories']:
                text += f"▫️ {cat_name}: <b>{count} ta</b> telefon\n"
        else:
            text += "<i>Kategoriyalar yo'q</i>\n"

        text += "\n➖➖➖➖➖➖➖➖➖➖\n"

        # 3. Oxirgi 5 ta User
        text += "👤 <b>Oxirgi 5 ta a'zo:</b>\n"
        if stats['last_users']:
            for user in stats['last_users']:
                text += f"🆕 {user[0]}\n"
        else:
            text += "<i>Hech kim yo'q</i>\n"

        text += "\n"

        # 4. Oxirgi 5 ta Telefon
        text += "📱 <b>Oxirgi 5 ta e'lon:</b>\n"
        if stats['last_products']:
            for prod in stats['last_products']:
                text += f"🆕 {prod[0]} — <b>{prod[1]}</b>\n"
        else:
            text += "<i>E'lonlar yo'q</i>\n"

        await message.answer(text)


# --- 3. KATEGORIYA QO'SHISH (TIKLANDI) ---
@router.message(F.text == "➕ Kategoriya qo'shish")
async def start_add_category(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Yangi kategoriya nomini yozing (masalan: Samsung):")
        await state.set_state(AdminState.waiting_for_category_name)


@router.message(AdminState.waiting_for_category_name)
async def finish_add_category(message: types.Message, state: FSMContext):
    db.add_category(message.text)
    await message.answer(f"✅ <b>{message.text}</b> kategoriyasi muvaffaqiyatli qo'shildi!",
                         reply_markup=get_admin_panel_buttons())
    await state.clear()


# --- 4. BAZANI ODDDIY KO'RISH (Jadvallar) ---
@router.message(F.text == "🗄 Bazani ko'rish")
async def show_raw_db(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        users = db.get_table_data("users")
        products = db.get_table_data("products")
        await message.answer(f"Hozir bazada:\nUsers: {len(users)}\nProducts: {len(products)}")


# --- 5. ORQAGA QAYTISH (TIKLANDI) ---
@router.message(F.text == "Bosh menyuga")
async def back_to_main(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Asosiy menyuga qaytdingiz:", reply_markup=get_user_main_menu())