from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS, MANAGER_URL

def get_menu_for_user(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦Создать заказ", callback_data='new_order')],
            [InlineKeyboardButton(text="👤Личный кабинет", callback_data='account')],
            [InlineKeyboardButton(text="💱 Текущий курс", callback_data='rates')],
            [InlineKeyboardButton(text="❓ FAQ", callback_data='faq')],
            [InlineKeyboardButton(text="💬 Связаться с нами", url=MANAGER_URL)]
        ]
    )
    if user_id in ADMIN_IDS:
        kb.inline_keyboard.insert(
            0,
            [InlineKeyboardButton(text="🛠 Админка", callback_data="admin_panel")])
    return kb