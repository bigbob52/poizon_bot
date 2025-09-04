from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from .keyboards.faq import faq_kb

router = Router()


@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите интересующий Вас вопрос из списка ниже",
        reply_markup=faq_kb
    )
    await callback.answer()