from aiogram import types, Router, F
from aiogram.filters import Command

from .common import send_main_menu
from db.users import add_user, get_user_by_id
from config import ADMIN_IDS, ADMIN_ALERT_NEW_USER
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id

    user = get_user_by_id(user_id)

    if not user:
        # добавляем в бд
        username = message.from_user.username or None
        add_user(user_id, username)

        # если надо, шлем увед админам о новом юзере
        text = (
            f"👤 Новый пользователь!\n\n"
            f"ID: <code>{user_id}</code>\n"
            f"Username: @{message.from_user.username or '—'}\n"
            f"Имя: {message.from_user.full_name}"
        )

        if ADMIN_ALERT_NEW_USER:
            for admin_id in ADMIN_IDS:
                try:
                    await message.bot.send_message(admin_id, text)
                except Exception as e:
                    logger.warning(f"Увед о регистрации юзера не отправился админу #{admin_id}. {e}")


    await send_main_menu(user_id, message)

@router.callback_query(F.data == "main_menu")
async def main_menu_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await send_main_menu(user_id, callback)
    await callback.answer()
