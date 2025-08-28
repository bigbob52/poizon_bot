from aiogram import Dispatcher
from aiogram import Router

from middlewares.admin_only import AdminOnlyMiddleware
from . import admin_panel, manage_orders, manage_users


admin_router = Router(name='admin')
admin_router.message.middleware(AdminOnlyMiddleware())
admin_router.callback_query.middleware(AdminOnlyMiddleware())

admin_router.include_router(admin_panel.router)
admin_router.include_router(manage_orders.router)
admin_router.include_router(manage_users.router)

def register_admin_handlers(dp: Dispatcher):
    dp.include_router(admin_router)