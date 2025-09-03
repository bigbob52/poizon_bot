from aiogram.types import CallbackQuery, Message
from keyboards.menu import get_menu_for_user


async def send_main_menu(user_id: int, destination: CallbackQuery | Message):
    """Отправка главного меню пользователю"""
    kb = get_menu_for_user(user_id)
    if isinstance(destination, Message):
        await destination.answer(
            text="Приветствую! 👋\n"
                 "Я ваш помощник в оформлении заказов.\n"
                 "Выберите нужное действие из меню ниже.",
            reply_markup=kb
        )
    elif isinstance(destination, CallbackQuery):
        await destination.message.edit_text(
            text="Приветствую! 👋\n"
                 "Я ваш помощник в оформлении заказов.\n"
                 "Выберите нужное действие из меню ниже.",
            reply_markup=kb
        )
        await destination.answer()