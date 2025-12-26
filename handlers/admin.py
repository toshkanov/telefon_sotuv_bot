from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMINS
from keywords.reply import get_admin_panel_buttons, get_admin_main_menu
from database import Database

router = Router()
db = Database()

# Reklama yuborish holatlari (States)
class BroadcastState(StatesGroup):
    waiting_for_message = State()

@router.message(F.text == "Admin Panel")
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Admin Panelga xush kelibsiz:", reply_markup=get_admin_panel_buttons())
    else:
        await message.answer("Siz admin emassiz!")

@router.message(F.text == "📊 Statistika")
async def show_stats(message: types.Message):
    if message.from_user.id in ADMINS:
        count = db.count_users()
        await message.answer(f"📊 Bazada jami foydalanuvchilar: {count} ta")

@router.message(F.text == "📢 Reklama yuborish")
async def ask_ad_message(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Reklama matnini yoki rasmini yuboring:")
        await state.set_state(BroadcastState.waiting_for_message)

@router.message(BroadcastState.waiting_for_message)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    # 1. Barcha userlarni olamiz (buni database.py ga qo'shish kerak bo'ladi, hozircha count bilan ishlaymiz)
    # Hozircha shunchaki adminni o'ziga test qilib yuboramiz
    await message.copy_to(chat_id=message.chat.id)
    await message.answer("Reklama (hozircha faqat sizga) yuborildi! (Database funksiyasini keyin kengaytiramiz)")
    await state.clear()