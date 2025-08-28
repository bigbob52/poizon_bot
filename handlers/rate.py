from aiogram import types, Router, F
import aiohttp
from async_lru import alru_cache

from handlers.keyboards.common import back_to_menu_kb
from service.exchange_rate import exchange_rate_cache
from config import RATE_MESSAGE_TEMPLATE


router = Router()

API_URL = f"https://v6.exchangerate-api.com/v6/1f82a3fb35170c63f5af7fd5/latest/CNY"


@router.callback_query(F.data == "rates")
async def show_rates(callback: types.CallbackQuery):
    rate = await exchange_rate_cache.fetch_exchange_rate()
    update_ts = exchange_rate_cache.last_update

    await callback.message.edit_text(
        RATE_MESSAGE_TEMPLATE.format(rate=rate, update_ts=update_ts),
        reply_markup=back_to_menu_kb
    )
    await callback.answer()
