from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
])