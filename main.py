from loader import bot, dp
from logger import setup_logger
from handlers import register_user_handlers
from admin import register_admin_handlers
from middlewares.admin_only import AdminOnlyMiddleware

from service.rate_updater import update_currency_message
import asyncio


async def main():
    setup_logger()
    register_user_handlers(dp)
    register_admin_handlers(dp)
    dp.update.middleware(AdminOnlyMiddleware())

    asyncio.create_task(update_currency_message())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())