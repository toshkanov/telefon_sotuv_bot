from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import CHANNEL_ID, ADMIN_USERNAME, CHANNEL_URL, ADMINS
from keywords.reply import get_user_main_menu, get_categories_buttons
from database import Database

router = Router()
db = Database()


# E'lon berish holatlari
class SellState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_category = State()


# --- 1. E'LON BERISH (Startapi) ---
@router.message(F.text == "➕ E'lon berish")
async def start_sell(message: types.Message, state: FSMContext):
    await message.answer("Telefon rasmini yuboring (faqat 1 ta rasm):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SellState.waiting_for_photo)


@router.message(SellState.waiting_for_photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    # Rasmni ID sini olib qolamiz
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
    # Kategoriya ID sini topamiz
    cat_name = message.text
    cat = db.execute("SELECT id FROM categories WHERE name=?", (cat_name,), fetchone=True)

    if not cat:
        await message.answer("Iltimos, tugmalardan birini tanlang!")
        return

    data = await state.get_data()
    # 1. Bazaga saqlaymiz
    db.add_product(data['name'], data['price'], cat[0], data['image'], message.from_user.id)

    # 2. KANALGA YUBORAMIZ 📢
    caption = (f"📱 <b>Yangi e'lon!</b>\n\n"
               f"🏷 <b>Model:</b> {data['name']}\n"
               f"💰 <b>Narxi:</b> {data['price']}\n"
               f"📂 <b>Kategoriya:</b> {cat_name}\n"
               f"👤 <b>Sotuvchi:</b> {message.from_user.mention_html()}\n\n"
               f"🤖 Bot orqali xarid qiling: @SizningBotingizUserneymi")

    try:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=data['image'], caption=caption, parse_mode="HTML")
        await message.answer("✅ E'loningiz qabul qilindi va kanalga joylandi!", reply_markup=get_user_main_menu())
    except Exception as e:
        await message.answer(f"Xatolik: Botni kanalga Admin qiling!\n{e}", reply_markup=get_user_main_menu())

    await state.clear()


# --- 2. TELEFONLAR BOZORI (Buyurtma berish) ---
@router.message(F.text == "📱 Telefonlar bozori")
async def show_market(message: types.Message):
    products = db.get_table_data("products")
    if not products:
        await message.answer("Hozircha sotuvda telefonlar yo'q.")
        return

    await message.answer("👇 Sotuvdagi telefonlar (Sotib olish uchun kodini yozing):")

    for prod in products:
        # prod = (id, name, price, cat_id, image, seller, desc)
        caption = f"🆔 Kod: <b>{prod[0]}</b>\n📱 {prod[1]} - {prod[2]}"
        await message.answer_photo(photo=prod[4], caption=caption, parse_mode="HTML")

    await message.answer("Sotib olish uchun telefon kodini yozing (masalan: 1)")


# --- 3. SOTIB OLISH LOGIKASI ---
@router.message(lambda x: x.text.isdigit())  # Agar user raqam yozsa
async def buy_product(message: types.Message, bot: Bot):
    prod_id = int(message.text)
    product = db.execute("SELECT * FROM products WHERE id=?", (prod_id,), fetchone=True)

    if product:
        # ADMINGA XABAR BORADI
        admin_text = (f"🚨 <b>YANGI BUYURTMA!</b>\n\n"
                      f"👤 <b>Mijoz:</b> {message.from_user.mention_html()}\n"
                      f"📱 <b>Telefon:</b> {product[1]}\n"
                      f"💰 <b>Narxi:</b> {product[2]}\n"
                      f"🆔 <b>Kod:</b> {product[0]}")

        # Hamma adminlarga jo'natamiz
        for admin in ADMINS:
            try:
                await bot.send_message(chat_id=admin, text=admin_text, parse_mode="HTML")
            except:
                pass

        await message.answer("✅ Buyurtmangiz Adminga yuborildi! Tez orada aloqaga chiqamiz.",
                             reply_markup=get_user_main_menu())
    else:
        await message.answer("Bunday kodli telefon topilmadi.")


# --- 4. QO'SHIMCHA MENYULAR ---
@router.message(F.text == "📢 Kanalimiz")
async def show_channel(message: types.Message):
    await message.answer(f"Bizning kanal: {CHANNEL_URL}")


@router.message(F.text == "👤 Admin bilan aloqa")
async def contact_admin(message: types.Message):
    await message.answer(f"Admin: {ADMIN_USERNAME}")