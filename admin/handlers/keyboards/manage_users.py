from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ITEMS_PER_PAGE
from math import ceil


users_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 Поиск юзера", callback_data="ask_user_identifier")],
    [InlineKeyboardButton(text="📋 Все пользователи", callback_data="get_all_users")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")]
])

def get_edit_user_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Изменить количество заказов", callback_data=f"ask_order_count:{user_id}")],
        [InlineKeyboardButton(text="🎁 Изменить количество баллов", callback_data=f"ask_bonus_count:{user_id}")],
        [InlineKeyboardButton(text="📝 Посмотреть заказы юзера", callback_data=f"ask_order_id:{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manage_users")]
    ])

def get_users_list_kb(users: list[dict], page: int = 1) -> InlineKeyboardMarkup:
    # считаем сколько страниц надо
    total_pages = max(1, ceil(len(users) / ITEMS_PER_PAGE))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_users = users[start:end]

    kb = InlineKeyboardBuilder()
    # добавляем в кб
    for user in page_users:
        user_id = user['user_id']
        username = user['username']
        kb.row(
            InlineKeyboardButton(
                text=f"👤 Юзер #{user_id} | @{username}" if username else f"👤 Юзер #{user_id}",
                callback_data=f"user_detail:{user_id}"
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"users_page:{page - 1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"users_page:{page + 1}")
        )

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="↩️ Назад в меню", callback_data="admin_panel"))
    return kb.as_markup()

back_to_users_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="manage_users")]
])