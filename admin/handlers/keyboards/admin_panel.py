from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📦 Заказы", callback_data='manage_orders')],
    [InlineKeyboardButton(text="⚙️ Пользователи", callback_data='manage_users')],
    [InlineKeyboardButton(text="📊 Статистика", callback_data='stats')],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data='main_menu')]
])
