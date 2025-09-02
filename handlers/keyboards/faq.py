from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import MANAGER_URL


faq_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒 Что такое Poizon?", url="https://t.me/PoizonBelarusShip/51")],
    [InlineKeyboardButton(text="📱 Установка приложения и регистрация в нем", url="https://t.me/PoizonBelarusShip/52")],
    [InlineKeyboardButton(text="🔍 Как искать товар?", url="https://t.me/PoizonBelarusShip/53")],
    [InlineKeyboardButton(text="👀 Как подобрать размер обуви/одежды?", url="https://t.me/PoizonBelarusShip/59")],
    [InlineKeyboardButton(text="💯 Точно ли на Poizon оригинал?", url="https://t.me/PoizonBelarusShip/60")],
    [InlineKeyboardButton(text="✈️ Какие у вас условия и сроки доставки?", url="https://t.me/PoizonBelarusShip/61")],
    [InlineKeyboardButton(text="✅ Как оформить заказ?", url="https://t.me/PoizonBelarusShip/62")],
    [InlineKeyboardButton(text="📞 Остались вопросы? Свяжитесь с нами", url=MANAGER_URL)],
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="main_menu")],
])