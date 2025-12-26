import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import CHANNEL_ID, ADMIN_USERNAME, CHANNEL_URL, ADMINS
from keywords.reply import get_user_main_menu, get_categories_buttons
from database import Database

router = Router()
db = Database()

# ⚠️ O'Z BOTINGIZ USERNAMESINI SHU YERGA YOZING!
MY_BOT_USERNAME = "@Mobil_Savdo_Markazi_bot"


# E'lon berish holatlari
class SellState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_category = State()


# ==================================================
# 1. YORDAMCHI BUYRUQLAR (Reset)
# ==================================================

# Agar bot qotib qolsa, shu buyruqni yozasiz: /cancel
@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Barcha jarayonlar bekor qilindi. Bosh menyudasiz.", reply_markup=get_user_main_menu())


# ==================================================
# 2. E'LON BERISH (Sotish)
# ==================================================

@router.message(F.text == "➕ E'lon berish")
async def start_sell(message: types.Message, state: FSMContext):
    await message.answer("Telefon rasmini yuboring (faqat 1 ta rasm):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SellState.waiting_for_photo)


@router.message(SellState.waiting_for_photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)
    await message.answer("Telefon modelini yozing (masalan: iPhone 13 Pro):")
    await state.set_state(SellState.waiting_for_name)


@router.message(SellState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Narxini yozing (masalan: 600$):")
    await state.set_state(SellState.waiting_for_price)


@router.message(SellState.waiting_for_price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Kategoriyani tanlang:", reply_markup=get_categories_buttons())
    await state.set_state(SellState.waiting_for_category)


@router.message(SellState.waiting_for_category)
async def finish_sell(message: types.Message, state: FSMContext, bot: Bot):
    try:
        cat_name = message.text
        cat = db.execute("SELECT id FROM categories WHERE name=?", (cat_name,), fetchone=True)

        if not cat:
            await message.answer("Iltimos, pastdagi tugmalardan birini tanlang!")
            return

        data = await state.get_data()
        # Bazaga saqlash
        db.add_product(data['name'], data['price'], cat[0], data['image'], message.from_user.id)

        # Kanalga chiqarish
        caption = (f"📱 <b>Yangi e'lon!</b>\n\n"
                   f"🏷 <b>Model:</b> {data['name']}\n"
                   f"💰 <b>Narxi:</b> {data['price']}\n"
                   f"📂 <b>Kategoriya:</b> {cat_name}\n"
                   f"👤 <b>Sotuvchi:</b> {message.from_user.mention_html()}\n\n"
                   f"🤖 <b>Sotib olish uchun botga kiring:</b>\n👉 {MY_BOT_USERNAME}")

        await bot.send_photo(chat_id=CHANNEL_ID, photo=data['image'], caption=caption, parse_mode="HTML")
        await message.answer("✅ E'loningiz qabul qilindi va kanalga joylandi!", reply_markup=get_user_main_menu())
        await state.clear()

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}", reply_markup=get_user_main_menu())
        await state.clear()


# ==================================================
# 3. BOZOR VA MENYULAR
# ==================================================

@router.message(F.text == "📱 Telefonlar bozori")
async def show_market(message: types.Message):
    products = db.get_table_data("products")
    if not products:
        await message.answer("Hozircha sotuvda telefonlar yo'q.")
        return

    await message.answer("👇 Sotuvdagi telefonlar:")
    for prod in products:
        caption = f"🆔 Kod: <b>{prod[0]}</b>\n📱 {prod[1]} - {prod[2]}"
        await message.answer_photo(photo=prod[4], caption=caption, parse_mode="HTML")

    await message.answer("Sotib olish uchun telefon kodini yozing (masalan: 1)")


@router.message(F.text == "📢 Kanalimiz")
async def show_channel(message: types.Message):
    await message.answer(f"Bizning kanal: {CHANNEL_URL}")


@router.message(F.text == "👤 Admin bilan aloqa")
async def contact_admin(message: types.Message):
    await message.answer(f"Admin: {ADMIN_USERNAME}")


# ==================================================
# 4. UNIVERSAL HANDLER (Buyurtma qabul qilish)
# ==================================================

@router.message()
async def handle_any_text(message: types.Message, bot: Bot, state: FSMContext):
    # 1. Agar foydalanuvchi "holat"da bo'lsa (masalan rasm yuborishi kerak), lekin yozuv yozsa:
    current_state = await state.get_state()
    if current_state:
        await message.answer("⚠️ Siz hozir e'lon berish jarayonidasiz.\nTo'xtatish uchun /cancel deb yozing.")
        return

    text = message.text
    # 2. Agar matn bo'lmasa (sticker va h.k.)
    if not text:
        await message.answer("Iltimos, faqat yozuv yoki raqam yuboring.")
        return

    # 3. RAQAM (ID) TEKSHIRISH
    if text.isdigit():
        prod_id = int(text)
        try:
            product = db.execute("SELECT * FROM products WHERE id=?", (prod_id,), fetchone=True)

            if product:
                # Adminga xabar
                admin_text = (f"🚨 <b>YANGI BUYURTMA!</b>\n\n"
                              f"🆔 <b>Kod:</b> {product[0]}\n"
                              f"📱 <b>Model:</b> {product[1]}\n"
                              f"💰 <b>Narxi:</b> {product[2]}\n"
                              f"👤 <b>Xaridor:</b> {message.from_user.mention_html()}")

                # Adminlarga yuborish
                count = 0
                for admin in ADMINS:
                    try:
                        await bot.send_message(chat_id=admin, text=admin_text, parse_mode="HTML")
                        count += 1
                    except Exception as e:
                        logging.error(f"Adminga yuborishda xato: {e}")

                if count > 0:
                    await message.answer(
                        "✅ <b>Buyurtmangiz qabul qilindi!</b>\nAdminlarimiz tez orada aloqaga chiqishadi.",
                        reply_markup=get_user_main_menu())
                else:
                    await message.answer("❌ Uzr, Adminlar bilan bog'lanib bo'lmadi. Keyinroq urinib ko'ring.")
            else:
                await message.answer("❌ Bunday kodli mahsulot topilmadi.")

        except Exception as e:
            await message.answer(f"Tizim xatosi: {e}")

    # 4. BOSHQA YOZUVLAR
    else:
        await message.answer("🤷‍♂️ Tushunmadim.\nSotib olish uchun mahsulot <b>kodini</b> (faqat raqam) yozing.",
                             reply_markup=get_user_main_menu())