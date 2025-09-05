from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ITEMS_PER_PAGE, STATUS_DISPLAY
from math import ceil


orders_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 Поиск по номеру заказа", callback_data="get_oder_by_id")],
    [InlineKeyboardButton(text="📋 Все заказы", callback_data="get_all_orders")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")]
])

def get_edit_order_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Изменить статус заказа", callback_data=f"ask_order_status:{order_id}")],
        [InlineKeyboardButton(text="🗑️ Удалить заказ", callback_data=f"ask_delete_order:{order_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manage_orders")]
    ])

def get_order_status_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=display, callback_data=f"set_order_status:{order_id}:{status}")]
        for status, display in STATUS_DISPLAY.items()
    ])

def get_delete_confirm_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, безвозвратно удалить заказ", callback_data=f"confirm_delete_order:{order_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_delete_order:{order_id}")]
    ])

def get_orders_list_kb(orders: list[dict], page: int = 1) -> InlineKeyboardMarkup:
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
                callback_data=f"order_detail:{order['order_id']}"
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"orders_page:{page-1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"orders_page:{page+1}")
        )

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="↩️ Назад в меню", callback_data="admin_panel"))
    return kb.as_markup()

