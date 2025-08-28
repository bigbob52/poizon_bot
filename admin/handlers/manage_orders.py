from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from admin.handlers.keyboards.manage_orders import *
from db.orders import update_order_status, delete_order, get_all_actual_orders
from .common import render_order


router = Router()

@router.callback_query(F.data == "manage_orders")
async def manage_orders(callback: CallbackQuery):
    await callback.message.edit_text("Что именно с ордерами делаем?", reply_markup=orders_kb)



async def show_all_orders(target):
    orders = get_all_actual_orders()
    if not orders:
        await target.message.edit_text("❌ Нет актуальных заказов")
        return

    await target.message.edit_text(
        "📋 Все актуальные заказы:",
        reply_markup=get_orders_list_kb(orders, page=1)
    )


# --- Поиск заказа по id ---
class OrderSearch(StatesGroup):
    order_id = State()

@router.callback_query(F.data == "get_oder_by_id")
async def ask_oder_id(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите номер заказа:")
    await state.set_state(OrderSearch.order_id)
    await callback.answer()

@router.message(OrderSearch.order_id)
async def get_order_by_id(message: Message, state: FSMContext):
    order_id = int(message.text.strip())
    await render_order(order_id, message)
    await state.clear()

@router.callback_query(F.data.startswith("ask_order_status:"))
async def ask_order_status(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[-1])
    await callback.message.edit_text(
        "Выберите новый статус для заказа из списка: ",
        reply_markup=get_order_status_kb(order_id)
    )

@router.callback_query(F.data.startswith("set_order_status:"))
async def set_order_status(callback: CallbackQuery):
    _, order_id, status = callback.data.split(":")
    order_id = int(order_id)

    update_order_status(order_id, status)

    await callback.message.edit_text(
        f"Статус заказа #{order_id} обновлен на {status}",
        reply_markup=get_edit_order_kb(order_id)
    )

@router.callback_query(F.data.startswith("ask_delete_order:"))
async def ask_delete_order(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        f"Вы уверены, что хотите удалить заказ #{order_id}? Это действие необратимо.",
        reply_markup=get_delete_confirm_kb(order_id)
    )

@router.callback_query(F.data.startswith("confirm_delete_order:"))
async def confirm_delete_order(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    delete_order(order_id)
    await callback.message.answer(f"🗑️ Заказ #{order_id} успешно удален")
    await show_all_orders(callback)


@router.callback_query(F.data.startswith("cancel_delete_order:"))
async def cancel_delete_order(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    # await callback.message.edit_text(
    #     f"Отмена удаления заказа #{order_id}",
    #     reply_markup=get_edit_order_kb(order_id)
    # )
    await render_order(order_id, callback, get_edit_order_kb(order_id))


# --- Получение всех актуальных заказов (new, accepted) ---
@router.callback_query(F.data == "get_all_orders")
async def get_all_orders(callback: CallbackQuery):
    await show_all_orders(callback)

# пагинация
@router.callback_query(F.data.startswith("orders_page:"))
async def paginate_orders(callback: CallbackQuery):
    page = int(callback.data.split(":")[-1])
    orders = get_all_actual_orders()
    await callback.message.edit_reply_markup(
        reply_markup=get_orders_list_kb(orders, page=page)
    )

@router.callback_query(F.data.startswith("order_detail:"))
async def show_order(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[-1])
    await render_order(order_id, callback, get_edit_order_kb(order_id))