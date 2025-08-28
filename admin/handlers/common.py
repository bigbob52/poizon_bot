from aiogram.types import CallbackQuery, Message

from admin.handlers.keyboards.manage_orders import *
from db.orders import get_order


async def render_order(order_id: int, target, reply_markup: InlineKeyboardMarkup | None = None):
    order_info, order_items = get_order(order_id)

    if not order_info:
        if isinstance(target, CallbackQuery):
            await target.message.edit_text("❌ Заказ не найден", reply_markup=orders_kb)
            await target.answer()
        else:
            await target.answer("❌ Заказ не найден", reply_markup=orders_kb)
        return

    text = (
            f"<b>Заказ #{order_info['order_id']}</b>\n"
            f"📊 Статус: {order_info['status']}\n"
            f"💰 Общая сумма: {sum(item['price'] for item in order_items)}¥\n"
            f"🆔 Telegram ID клиента: <code>{order_info['user_id']}</code>\n"
            f"🗓️ Заказ создан: {order_info['created_at']} UTC\n\n" +
            "\n\n".join(
                [f"Товар №{i + 1}.\n"
                 f"🔗 Ссылка: {item['link']}\n"
                 f"📏 Размер: {item['size']}\n"
                 f"🏷️ Цена: {item['price']}¥"
                 for i, item in enumerate(order_items)]
            )
    )

    # если разметка не передана — ставим дефолтную клавиатуру редактирования
    if not reply_markup:
        reply_markup = get_edit_order_kb(order_id)

    if isinstance(target, CallbackQuery):
        # редактируем сообщение, из которого пришёл callback
        await target.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        await target.answer()  # закрываем "часики" Telegram
    elif isinstance(target, Message):
        # отправляем новое сообщение, если это обычный текст от пользователя
        await target.answer(text, reply_markup=reply_markup, parse_mode="HTML")
