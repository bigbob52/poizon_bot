from aiogram import types, Router, F
from db.users import get_user_by_id
from handlers.keyboards.common import back_to_menu_kb

router = Router()

@router.callback_query(F.data == "account")
async def account_handler(callback: types.CallbackQuery):
    user = get_user_by_id(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"Личный кабинет:\n\n"
            f"ID {user['user_id']}\n"
            f"Ник: {user['username']}\n"
            f"Всего заказов: {user['orders']}\n"
            f"Бонусов: {user['bonus']} BYN",
            reply_markup=back_to_menu_kb
        )
        await callback.answer()

    else:
        await callback.answer("Не удалось открыть личный кабинет :(")
