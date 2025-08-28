from aiogram import types, Dispatcher

async def instruction_handler(callback: types.CallbackQuery):
    await callback.message.answer("Инструкция по использованию 📖 (пока заглушка).")
    await callback.answer()

async def reviews_handler(callback: types.CallbackQuery):
    await callback.message.answer("Отзывы ⭐ (пока заглушка).")
    await callback.answer()

async def guarantee_handler(callback: types.CallbackQuery):
    await callback.message.answer("Наши гарантии ✅ (пока заглушка).")
    await callback.answer()

def register_other(dp: Dispatcher):
    dp.callback_query.register(instruction_handler, lambda c: c.data == "instruction")
    dp.callback_query.register(reviews_handler, lambda c: c.data == "reviews")
    dp.callback_query.register(guarantee_handler, lambda c: c.data == "guarantee")
