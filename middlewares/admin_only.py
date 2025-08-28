from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from typing import Callable, Dict, Any, Awaitable
from config import ADMIN_IDS


class AdminOnlyMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:

        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        user_id = event.from_user.id


        if user_id not in ADMIN_IDS:
            if isinstance(event, CallbackQuery):
                await event.answer("❌ Нет доступа", show_alert=True)
            else:
                await event.answer("❌ У вас нет доступа")
            return  # прерываем выполнение хэндлера

        return await handler(event, data)