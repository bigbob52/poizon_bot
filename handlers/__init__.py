from aiogram import Dispatcher
from . import start, new_order, rate, account

def register_user_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(new_order.router)
    dp.include_router(rate.router)
    dp.include_router(account.router)
