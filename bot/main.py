import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import get_settings
from bot.database.engine import create_tables, session_maker
from bot.handlers import get_all_routers
from bot.middlewares.db import DatabaseMiddleware


async def on_startup():
    await create_tables()
    logging.info("Database tables created")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    settings = get_settings()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.update.middleware(DatabaseMiddleware(session_pool=session_maker))
    dp.include_router(get_all_routers())
    dp.startup.register(on_startup)

    logging.info("Bot is starting...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
