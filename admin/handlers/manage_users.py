from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from .keyboards.manage_users import users_kb, get_edit_user_kb, get_users_list_kb, back_to_users_panel_kb
from .keyboards.manage_orders import get_orders_list_kb
from db.users import get_user_by_id, get_user_by_username, update_orders, update_bonus, get_all_users
from db.orders import get_user_orders

router = Router()

class UserSearch(StatesGroup):
    user_identifier = State()

class EditUserStates(StatesGroup):
    waiting_for_order_count = State()
    waiting_for_bonus_count = State()

async def render_user(user_data: dict, target, reply_markup: InlineKeyboardMarkup | None = None):
    if not user_data:
        if isinstance(target, CallbackQuery):
            await target.message.edit_text("❌ Пользователь не найден", reply_markup=users_kb)
            await target.answer()
        else:
            await target.edit_text("❌ Пользователь не найден", reply_markup=users_kb)
        return

    user_id = user_data['user_id']
    username = user_data['username']

    text = (
            f"<b>Пользователь #{user_id}</b>\n\n"
            f"🆔 Telegram ID: <code>{user_id}</code>\n"
            f"👤 Username: {'@'+username if username else '--'}\n"
            f"📦 Всего заказов: {user_data['orders']}\n"
            f"🎁 Всего бонусов: {user_data['bonus']} BYN\n"
            f"🗓️ Зарегистрирован: {user_data['created_at']} UTC\n\n"
    )

    # если reply не передана — ставим дефолтную клавиатуру редактирования
    if reply_markup is None:
        reply_markup = get_edit_user_kb(user_id)

    if isinstance(target, CallbackQuery):
        # редактируем сообщение, из которого пришёл callback
        await target.message.edit_text(text, reply_markup=reply_markup)
        await target.answer()
    elif isinstance(target, Message):
        # отправляем новое сообщение, если это обычный текст от пользователя
        await target.edit_text(text, reply_markup=reply_markup)


@router.callback_query(F.data == "manage_users")
async def manage_users(callback: CallbackQuery):
    await callback.message.edit_text("Что с юзерами делаем?", reply_markup=users_kb)


# --- Поиск юзера по id или username ---
@router.callback_query(F.data == "ask_user_identifier")
async def ask_user_identifier(callback: CallbackQuery, state: FSMContext):
    bot_msg = await callback.message.edit_text(
        "Введите идентификатор пользователя:\n\n"
        "<i>Поддерживается поиск по id в формате <code>400939786</code> и по username <code>@username</code></i>",
        reply_markup=back_to_users_panel_kb
    )
    await state.set_state(UserSearch.user_identifier)
    await state.update_data(bot_message=bot_msg)
    await callback.answer()

@router.message(UserSearch.user_identifier)
async def get_user_identifier(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    bot_msg = data["bot_message"]

    user_identifier = message.text.strip()
    if user_identifier.isdigit():
        user_data = get_user_by_id(int(user_identifier))
    elif user_identifier[0] == '@':
        user_data = get_user_by_username(user_identifier[1:])
    else:
        await bot_msg.edit_text("Некорректный введенный идентификатор :(\n\n Введите тег, либо юзернейм через @")
        return

    await render_user(user_data, bot_msg)
    await state.clear()

@router.callback_query(F.data == "back_to_users_panel")
async def cancel_searching(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("❌ Поиск отменен", show_alert=False)
    await callback.message.edit_text("Что с юзерами делаем?", reply_markup=users_kb)



@router.callback_query(F.data.startswith("ask_order_count:"))
async def ask_order_count(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.update_data(user_id=user_id)
    await callback.message.answer(f"Введите новое кол-во закзов для юзера #{user_id}: ")
    await state.set_state(EditUserStates.waiting_for_order_count)
    await callback.answer()

@router.message(EditUserStates.waiting_for_order_count)
async def set_order_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌Введите число!")
        return

    data = await state.get_data()
    user_id = data["user_id"]
    order_count = int(message.text)
    update_orders(user_id, order_count)

    await message.answer(f"✅ Новое количество заказов пользователя #{user_id}: {order_count}")
    await state.clear()

@router.callback_query(F.data.startswith("ask_bonus_count:"))
async def ask_bonus_count(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.update_data(user_id=user_id)
    await callback.message.answer(f"Введите новое кол-во баллов для юзера #{user_id}: ")
    await state.set_state(EditUserStates.waiting_for_bonus_count)
    await callback.answer()

@router.message(EditUserStates.waiting_for_bonus_count)
async def set_bonus_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌Введите число!")
        return

    data = await state.get_data()
    user_id = data["user_id"]
    bonus_count = int(message.text)
    update_bonus(user_id, bonus_count)

    await message.answer(f"✅ Новое количество бонусов пользователя #{user_id}: {bonus_count}")
    await state.clear()


@router.callback_query(F.data.startswith("ask_order_id:"))
async def ask_user_orders(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    orders = get_user_orders(user_id)

    if not orders:
        await callback.answer("❌ У пользователя нет заказов", show_alert=True)
        return

    await callback.message.edit_text(
        f"Список заказов пользователя #{user_id}",
        reply_markup=get_orders_list_kb(orders)
    )
    await callback.answer()

# --- Просмотр всех юзеров ---
async def show_all_users(target: Message | CallbackQuery):
    users = get_all_users()
    if not users:
        await target.message.edit_text("❌ Нет актуальных заказов")
        return

    await target.message.edit_text(
        "📋 Все юзеры:",
        reply_markup=get_users_list_kb(users, page=1)
    )

@router.callback_query(F.data == "get_all_users")
async def get_all_users_(callback: CallbackQuery):
    await show_all_users(callback)
    await callback.answer()

# пагинация
@router.callback_query(F.data.startswith("users_page:"))
async def paginate_users_list(callback: CallbackQuery):
    page = int(callback.data.split(":")[-1])
    users = get_all_users()
    await callback.message.edit_reply_markup(
        reply_markup=get_users_list_kb(users, page=page)
    )

@router.callback_query(F.data.startswith("user_detail:"))
async def show_user(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[-1])
    await render_user(
        user_data=get_user_by_id(user_id),
        target=callback,
        reply_markup=get_edit_user_kb(user_id)
    )
    await callback.answer()
