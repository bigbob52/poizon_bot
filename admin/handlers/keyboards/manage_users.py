from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



users_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 Поиск юзера", callback_data="ask_user_identifier")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")]
])


def get_edit_user_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Изменить количество заказов", callback_data=f"ask_order_count:{user_id}")],
        [InlineKeyboardButton(text="🎁 Изменить количество баллов", callback_data=f"ask_bonus_count:{user_id}")],
        [InlineKeyboardButton(text="📝 Посмотреть заказы юзера", callback_data=f"ask_order_id:{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manage_users")]
    ])
