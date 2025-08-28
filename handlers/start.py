from mailbox import Message

from aiogram import types, Router, F
from aiogram.filters import Command

from keyboards.menu import get_menu_for_user
from db.users import add_user
from config import ADMIN_IDS


router = Router()

async def send_main_menu(user_id: int, destination: types.CallbackQuery | types.Message):
    """Отправка главного меню пользователю"""
    kb = get_menu_for_user(user_id)
    if isinstance(destination, types.Message):
        await destination.answer(
            "Здарова, я бот! Выбирай кнопку",
            reply_markup=kb
        )
    elif isinstance(destination, types.CallbackQuery):
        await destination.message.edit_text(
            "Здарова, я бот! Выбирай кнопку",
            reply_markup=kb
        )
        await destination.answer()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or None
    add_user(user_id, username)

    await send_main_menu(user_id, message)


@router.callback_query(F.data == "main_menu")
async def main_menu_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await send_main_menu(user_id, callback)
    await callback.answer()
