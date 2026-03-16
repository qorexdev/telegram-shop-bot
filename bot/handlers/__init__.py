from aiogram import Router

from bot.handlers.admin import admin_router
from bot.handlers.cart import cart_router
from bot.handlers.order import order_router
from bot.handlers.user import user_router


def get_all_routers() -> Router:
    router = Router()
    router.include_router(admin_router)
    router.include_router(user_router)
    router.include_router(cart_router)
    router.include_router(order_router)
    return router
