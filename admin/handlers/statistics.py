from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timedelta, timezone

from .keyboards.statistics import stats_kb, back_to_stats_kb
from db.users import count_all_users, count_users_for_period
from db.orders import count_all_orders, count_orders_for_period

router = Router()


async def show_general_stats(callback: CallbackQuery):
    users_count = count_all_users()
    orders_count = count_all_orders()

    text = (
        f"<b>📊 Общая Статистика</b>\n\n"
        f"👤 <b>Пользователей:</b> {users_count}\n"
        f"📦 <b>Заказов:</b> {orders_count}"
    )

    await callback.message.edit_text(text=text, reply_markup=stats_kb)
    await callback.answer()


@router.callback_query(F.data == "stats")
async def statistics(callback: CallbackQuery):
    await show_general_stats(callback)

@router.callback_query(F.data.startswith("stats_for:"))
async def stats_for_period(callback: CallbackQuery):
    period = callback.data.split(":")[-1]

    now = datetime.now(timezone.utc)
    match period:
        case "1h":
            start_time = now - timedelta(hours=1)
            label = "Последний час"
        case "12h":
            start_time = now - timedelta(hours=12)
            label = "Последние 12 часов"
        case "24h":
            start_time = now - timedelta(hours=24)
            label = "Последние 24 часа"
        case "week":
            start_time = now - timedelta(days=7)
            label = "Неделя"
        case "month":
            start_time = now - timedelta(days=30)
            label = "Месяц"

    users_count = count_users_for_period(start_time)
    orders_count = count_orders_for_period(start_time)

    text = (
        f"<b>📊 Статистика за период: {label}</b>\n\n"
        f"👤 Зарегистрировалось пользователей: {users_count}\n"
        f"📦 Новых заказов: {orders_count}"
    )

    await callback.message.edit_text(text=text, reply_markup=back_to_stats_kb)
    await callback.answer()

@router.callback_query(F.data == "back_to_stats")
async def back_to_stats(callback: CallbackQuery):
    await show_general_stats(callback)
    await callback.answer()