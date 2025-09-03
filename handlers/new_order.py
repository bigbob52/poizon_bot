from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

from config import MANAGER_ID
from db.orders import create_order, update_order_status
from keyboards.menu import get_menu_for_user

from handlers.keyboards.new_order import *


router = Router()

class OrderFSM(StatesGroup):
    link = State()
    size = State()
    price = State()

async def show_current_order(message: Message, items: list):
    """Отображение текущего заказа"""
    if items:
        await message.answer(
            f"<b>📦 Ваш заказ:</b>\n\n" +
            "\n\n".join(
                [
                    f"<u>Позиция №{i+1}</u>\n"
                    f"<b>Товар:</b> {item['link']}\n"
                    f"<b>Размер:</b> {item['size']}\n"
                    f"<b>Цена:</b> {item['price']}¥"
                    for i, item in enumerate(items)
                ]
            ) + "\n\n"
            f"<b>💰 Общая сумма: {sum(item['price'] for item in items)}¥</b>",
            reply_markup=manage_order_kb
        )
    else:
        await message.answer("Ваш заказ пуст. Добавьте новый товар", reply_markup=empty_order_kb)

async def save_item_field(state: FSMContext, field_name: str, value):
    """Сохранение поля айтема"""
    data = await state.get_data()
    items = data.get("items", [])
    edit_index = data.get("edit_index")

    if edit_index is not None:
        # редактируем существующий товар
        items[edit_index][field_name] = value
        await state.update_data(items=items, edit_index=None)
        return items, True  # True — значит редактировали
    else:
        # добавляем новое поле в будущий товар
        await state.update_data(**{field_name: value})
        return items, False  # False — значит добавляем новый товар


# --- 1. Начало заказа ---
@router.callback_query(F.data == "new_order")
async def new_order_handler(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "<b>ℹ️ Перед началом оформления заказа рекомендуем ознакомиться с инструкцией (FAQ).</b>\n\n"
            "Зафиксированная ботом цена может быть скорректирована из-за изменений курса юаня и наличия товара на складах поставщика. "
            "Точную сумму менеджер сообщит вам персонально после оформления заказа."
        ),
        reply_markup=approval_kb
    )
    await callback.answer()


# --- 2. Пользователь согласился ---
@router.callback_query(F.data == "get_item_link")
async def ask_item_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔗 Отправьте ссылку на товар: ", reply_markup=help_link_kb)
    await state.set_state(OrderFSM.link)
    await callback.answer()


# --- 3. Проверка ссылки ---
@router.message(StateFilter(OrderFSM.link))
async def ask_item_size(message: Message, state: FSMContext):

    url_regex = r'https?://[^\s]+'
    allowed_prefixes = (
        "https://dw4.co/t/A/",
        "https://fast.dewu.com/page/productDetail"
    )

    urls = re.search(url_regex, message.text.strip())
    if not urls:
        await message.answer(
            "❌ В вашем сообщении не было найдено ссылки.\n"
            "Пожалуйста, отправьте корректную ссылку с Poizon"
        )

    url = urls.group(0)
    if not any(url.startswith(prefix) for prefix in allowed_prefixes):
        await message.answer(
            "❌ Ссылка должна быть с сайта Poizon\n"
            "Пожалуйста, проверьте вашу ссылку и пришлите ее",
            reply_markup=help_link_kb
        )
        return

    items, is_edited = await save_item_field(state, "link", url)

    if is_edited:
        await message.answer("✅ Ссылка обновлена!")
        await show_current_order(message, items)
    else:

        await message.answer(
            text=(
                "✅ Ссылка принята!\n"
                "Теперь укажите размер товара\n"
                "Если у товара нет — размера, поставьте «<code>—</code>»"
            ),
            reply_markup=help_size_kb,
        )
        await state.set_state(OrderFSM.size)


# --- 4. Сохраняем размер ---
@router.message(StateFilter(OrderFSM.size))
async def ask_item_price(message: Message, state: FSMContext):
    # todo: можно сделать обработчик тоже типа isdigit() или in (M, L, XL...)
    size = message.text.strip()
    items, is_edited = await save_item_field(state, "size", size)
    if is_edited:
        await message.answer("✅ Размер обновлен!")
        await show_current_order(message, items)
    else:
        await message.answer(
            text=(
                "✅ Размер сохранен!\n "
                "Теперь введите цену товара в юанях (CNY)."
            ),
            reply_markup=help_price_kb)
        await state.set_state(OrderFSM.price)


# --- 5. Сохраняем цену ---
@router.message(StateFilter(OrderFSM.price))
async def add_item_to_order(message: Message, state: FSMContext):
    price_text = message.text.strip()

    if not price_text.isdigit():
        await message.answer(
            "❌ Цена должна быть числом!",
            reply_markup=help_price_kb
        )
        return

    price = int(price_text)
    items, is_edited = await save_item_field(state, "price", price)

    if is_edited:
        await message.answer("✅ Цена обновлена!")
        await show_current_order(message, items)
    else:
        data = await state.get_data()
        link = data.get("link")
        size = data.get("size")

        items.append({"link": link, "size": size, "price": price})

        await state.update_data(items=items)
        await show_current_order(message, items)


# --- 6. Обработка финальных кнопок ---
# -- ADD --
@router.callback_query(F.data == "order_add")
async def add_more(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Добавляем новый товар в заказ!\n\n"
                                  "Отправь ссылку на новый товар: ")
    await state.set_state(OrderFSM.link)
    await callback.answer()

# -- EDIT --
# выбираем какой товар редачить
@router.callback_query(F.data == "order_edit")
async def edit_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("items", [])

    if not items:
        await callback.message.answer("У вас пока нет товаров для редактирования.")
        await callback.answer()
        return

    await callback.message.edit_text("Выберите товар для редактирования:", reply_markup=get_items_list_kb(items))
    await callback.answer()

# выбираем что редачить у товара, либо удаляем его
@router.callback_query(F.data.startswith("edit_item_"))
async def edit_item(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split("_")[-1])  # какой товар выбрали
    await state.update_data(edit_index=index)  # сохраняем индекс в state


    data = await state.get_data()
    item = data["items"][index]


    await callback.message.edit_text(
        f"Вы редактируете позицию №{index+1}:\n"
        f"Ссылка: {item['link']}\n"
        f"Размер: {item['size']}",
        reply_markup=edit_item_kb
    )
    await callback.answer()

# редачим ссылку
@router.callback_query(F.data == "edit_link")
async def edit_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте новую ссылку на товар: ")
    await state.set_state(OrderFSM.link)
    await callback.answer()

# редачим размер
@router.callback_query(F.data == "edit_size")
async def edit_size(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте новый размер товара: ")
    await state.set_state(OrderFSM.size)
    await callback.answer()

# редачим размер
@router.callback_query(F.data == "edit_price")
async def edit_size(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте новую цену товара: ")
    await state.set_state(OrderFSM.price)
    await callback.answer()

# удаляем товар
@router.callback_query(F.data == "delete_item")
async def delete_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("edit_index")
    items = data.get("items", [])

    if index is not None and 0 <= index < len(items):
        removed = items.pop(index)
        await state.update_data(items=items, edit_index=None)
        await callback.message.answer("✅ Товар успешно удален из заказа")
    else:
        await callback.message.answer("❌ Не удалось удалить товар")

    # выводим обновленный список товаров
    await show_current_order(callback.message, items)
    await callback.answer()

# ничего не делаем, возвращаемся в заказ
@router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("items", [])

    await show_current_order(callback.message, items)
    await callback.answer()

# -- SUBMIT --
# отправляем в канал менеджерам, добавляем в бд
@router.callback_query(F.data == "order_submit")
async def submit_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("items", [])
    user = callback.from_user

    if not items:
        await callback.message.answer(f"❌ Ваш заказ пуст. Добавьте товары")
        await callback.answer()
        return

    # сохраняем в бд
    order_id = create_order(user.id, items)

    # текст для менеджера
    order_text = (
        f"<b> Новый заказ #{order_id}!</b>\n"
        f"📊 Статус: new\n\n"
        f"👤 Клиент: @{user.username or user.full_name}\n"
        f"🆔 Telegram ID: <code>{user.id}</code>\n\n"
        f"💰Общая сумма заказа: {sum(item['price'] for item in items)}¥\n\n"
        + "\n\n".join(
            [f"Товар №{i+1}.\n"
             f"🔗 Ссылка: {item['link']}\n"
             f"📏 Размер: {item['size']}\n"
             f"🏷️ Цена: {item['price']}¥"
             for i, item in enumerate(items)]
        )
    )

    await callback.bot.send_message(
        chat_id=MANAGER_ID,
        text=order_text,
        disable_web_page_preview=True,
        reply_markup=get_manager_approval_kb(order_id)
    )

    await callback.message.edit_text(
        text=(
            f"✅ Заказ #{order_id} принят!\n\n"
            f"Наш менеджер уже получил уведомление и свяжется с вами в течение часа для уточнения всех деталей. Пожалуйста, ожидайте.\n\n"
            f"<i>Спасибо, что выбрали нас!</i> 🩵"
        ),
        reply_markup= None
    )
    await state.clear()

    # возвращаем в мейн меню
    await callback.message.answer(
        "🏠 Вы вернулись в главное меню",
        reply_markup=get_menu_for_user(user.id)
    )
    await callback.answer()


# -- FOR MANAGERS --
@router.callback_query(F.data.startswith("manager_order_accept_"))
async def manager_order_accept(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[-1])
    update_order_status(order_id, "accepted")
    new_text = callback.message.text.replace("Статус: new", "Статус: accepted")

    await callback.message.edit_reply_markup(None)  # убираем кнопки
    await callback.message.edit_text(
        text=new_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer("Заказ принят ✅")

@router.callback_query(F.data.startswith("manager_order_canceled_"))
async def manager_order_cancel(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[-1])
    update_order_status(order_id, "canceled")
    new_text = callback.message.text.replace("Статус: new", "Статус: canceled")

    await callback.message.edit_reply_markup(None)  # убираем кнопки
    await callback.message.edit_text(
        text=new_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await callback.answer("Заказ отклонен ❌")