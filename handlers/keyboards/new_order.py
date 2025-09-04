from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MANAGER_URL

approval_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Всё понятно, продолжаем", callback_data='get_item_link')],
    [InlineKeyboardButton(text="❓ FAQ", url='https://t.me/BelarusPoizonShip/8')],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="cancel_order")]
])

help_link_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❓ Где найти ссылку?", url="https://t.me/PoizonBelarusShip/62")],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="cancel_order")]
])

help_size_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❓ Как выбрать размер?", url="https://t.me/PoizonBelarusShip/62")],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="cancel_order")]
])

help_price_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❓ Где найти цену?", url="https://t.me/PoizonBelarusShip/62")],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="cancel_order")]
])

manage_order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="order_add")],
    [InlineKeyboardButton(text="✏️ Редактировать", callback_data="order_edit")],
    [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="order_submit")]
])

empty_order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить товар в заказ", callback_data="get_item_link")]
])

def get_items_list_kb(items):
    kb = InlineKeyboardBuilder()

    for i, item in enumerate(items):
        kb.row(
            InlineKeyboardButton(
                text=f"Позиция №{i + 1}",
                callback_data=f"edit_item_{i}"
            )
        )

    kb.row(InlineKeyboardButton(text="↩️ Вернуться к заказу", callback_data="cancel_editing"))

    return kb.as_markup()

edit_item_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 Изменить ссылку", callback_data="edit_link")],
    [InlineKeyboardButton(text="📏 Изменить размер", callback_data="edit_size")],
    [InlineKeyboardButton(text="🏷️ Изменить цену", callback_data="edit_price")],
    [InlineKeyboardButton(text="❌ Удалить из заказа", callback_data="delete_item")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="order_edit")],
])

final_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏠Вернуться в меню ")]
])

manager_link_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📞 Связаться с менеджером", url=MANAGER_URL)]
])

# MANAGERS
def get_manager_approval_kb(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data=f"manager_order_accept:{order_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"manager_order_cancel:{order_id}")]
    ])

manager_confirm_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Отправить пользователю", callback_data="confirm_cancel_comment")],
    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_cancel_process")]
])