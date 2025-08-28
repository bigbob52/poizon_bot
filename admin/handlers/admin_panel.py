from aiogram import Router, types, F
from admin.handlers.keyboards.admin_panel import admin_kb


router = Router()

@router.callback_query(F.data == "admin_panel", flags={"admins_only": True})
async def admin_panel(callback: types.CallbackQuery):
    await callback.message.edit_text("ку админ! че делать будем?", reply_markup=admin_kb)
    await callback.answer()
