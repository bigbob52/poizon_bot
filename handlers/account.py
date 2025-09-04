from aiogram import Router, F
from aiogram.types import CallbackQuery

from db.users import get_user_by_id
from db.orders import get_user_orders, get_order
from .common import send_main_menu
from .keyboards.account import account_kb, back_to_account_kb, get_user_orders_list_kb


router = Router()


async def render_account(callback: CallbackQuery):
    user = get_user_by_id(callback.from_user.id)

    if user:
        text = (
            f"<b>👤 Личный кабинет</b>\n\n"
            f"🆔 Ваш ID: <code>{user['user_id']}</code>\n\n"
            f"📦 Всего заказов: {user['orders']}\n"
            f"🎁 Всего бонусов: {user['bonus']} BYN"
        )

        if user['username'] is None:
            text += (
                "⚠️ <b>Внимание! У вас отсутствует публичный тег (@username)!</b>\n"
                "В связи с этим наш менеджер не сможет с вами связаться.\n"
                "Пожалуйста, добавьте юзернейм в настройках Telegram, либо свяжитесь с менеджером самостоятельно."
            )

        await callback.message.edit_text(
            text=text,
            reply_markup=account_kb
        )
        await callback.answer()

    else:
        await callback.answer("Не удалось открыть личный кабинет :(")



@router.callback_query(F.data == "account")
async def account_handler(callback: CallbackQuery):
    await render_account(callback)


@router.callback_query(F.data == "check_user_orders")
async def check_user_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    orders = get_user_orders(user_id)

    if not orders:
        await callback.message.edit_text(
            text="📭 У вас пока нет заказов.",
            reply_markup=back_to_account_kb
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        text="📦 Ваши заказы:",
        reply_markup=get_user_orders_list_kb(orders)
    )
    await callback.answer()

# пагинация
@router.callback_query(F.data.startswith("user_orders_page:"))
async def paginate_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    orders = get_user_orders(user_id)
    page = int(callback.data.split(":")[-1])

    await callback.message.edit_reply_markup(
        reply_markup=get_user_orders_list_kb(orders, page=page)
    )
    await callback.answer()

# --- показать конкретный заказ ---
@router.callback_query(F.data.startswith("user_order_detail:"))
async def show_user_order_detail(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    order_info, order_items = get_order(order_id)

    if not order_info or order_info["user_id"] != callback.from_user.id:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return

    text = (
        f"<b>Заказ #{order_info['order_id']}</b>\n"
        # f"📊 Статус: {order_info['status']}\n"
        f"💰 Общая сумма: {sum(item['price'] for item in order_items)}¥\n"
        f"🗓️ Создан: {order_info['created_at']} UTC\n\n" +
        "\n\n".join(
            [f"<u>Позиция №{i+1}</u>\n"
             f"🔗 Ссылка: {item['link']}\n"
             f"📏 Размер: {item['size']}\n"
             f"🏷️ Цена: {item['price']}¥"
             for i, item in enumerate(order_items)]
        )
    )

    await callback.message.edit_text(text, reply_markup=back_to_account_kb)
    await callback.answer()



@router.callback_query(F.data == "back_to_account")
async def back_to_account(callback: CallbackQuery):
    await render_account(callback)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await send_main_menu(callback.from_user.id, callback)