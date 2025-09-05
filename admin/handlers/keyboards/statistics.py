from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


stats_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1Ч", callback_data="stats_for:1h"),
        InlineKeyboardButton(text="12Ч", callback_data="stats_for:12h"),
        InlineKeyboardButton(text="24Ч", callback_data="stats_for:24h"),
    ],
    [
        InlineKeyboardButton(text="Неделя", callback_data="stats_for:week"),
        InlineKeyboardButton(text="Месяц", callback_data="stats_for:month")
    ],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")],
])

back_to_stats_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_stats')]
])