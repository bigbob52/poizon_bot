from loader import bot, dp
from logger import setup_logger
from config import MANAGER_ID

import asyncio


async def main():
    setup_logger()
    await bot.send_message(MANAGER_ID, "123")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())