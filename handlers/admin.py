from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMINS
# Diqqat: Bu yerda endi xato bermaydi
from keywords.reply import get_admin_panel_buttons, get_user_main_menu
from database import Database

router = Router()
db = Database()

class AdminState(StatesGroup):
    waiting_for_category_name = State()

@router.message(F.text == "Admin Panel")
async def admin_panel(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Admin Panel:", reply_markup=get_admin_panel_buttons())

@router.message(F.text == "➕ Kategoriya qo'shish")
async def start_add_category(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Kategoriya nomini yozing (masalan: Samsung):")
        await state.set_state(AdminState.waiting_for_category_name)

@router.message(AdminState.waiting_for_category_name)
async def finish_add_category(message: types.Message, state: FSMContext):
    db.add_category(message.text)
    await message.answer(f"✅ {message.text} qo'shildi!", reply_markup=get_admin_panel_buttons())
    await state.clear()

@router.message(F.text == "🗄 Bazani ko'rish")
async def show_db_stats(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        products = db.get_table_data("products")
        users = db.get_table_data("users")
        await message.answer(f"📊 Statistika:\n👤 Userlar: {len(users)}\n📱 E'lonlar: {len(products)}")

@router.message(F.text == "Bosh menyuga")
async def back_to_main(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Asosiy menyu:", reply_markup=get_user_main_menu())