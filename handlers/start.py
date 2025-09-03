from aiogram import types, Router, F
from aiogram.filters import Command

from .common import send_main_menu
from db.users import add_user


router = Router()

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
