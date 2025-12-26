from aiogram import Router, types

router = Router()

@router.message()
async def echo_handler(message: types.Message):
    # Foydalanuvchi yozgan xabarni o'ziga qaytarmaymiz, shunchaki ogohlantiramiz
    await message.answer("Tushunmadim 🤷‍♂️\nIltimos, pastdagi tugmalardan birini tanlang 👇")