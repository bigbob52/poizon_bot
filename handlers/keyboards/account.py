from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from math import ceil

from config import ITEMS_PER_PAGE, STATUS_DISPLAY



account_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📦 Мои заказы", callback_data="check_user_orders")],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="back_to_menu")]
])

back_to_account_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ Вернуться к аккаунту", callback_data="back_to_account")]
])

def get_user_orders_list_kb(orders: list[dict], page=1) -> InlineKeyboardMarkup:
    # считаем сколько страниц надо
    total_pages = max(1, ceil(len(orders) / ITEMS_PER_PAGE))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_orders = orders[start:end]

    kb = InlineKeyboardBuilder()
    # добавляем в кб
    for order in page_orders:
        kb.row(
            InlineKeyboardButton(
                text=f"Заказ #{order['order_id']} | {STATUS_DISPLAY[order['status']]}",
                callback_data=f"user_order_detail:{order['order_id']}"
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"user_orders_page:{page - 1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"user_orders_page:{page + 1}")
        )

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="↩️ Вернуться к аккаунту", callback_data="back_to_account"))
    return kb.as_markup()