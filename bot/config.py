import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    admin_id: int
    db_url: str = "sqlite+aiosqlite:///shop.db"


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN")
    admin_id = os.getenv("ADMIN_ID")

    if not token:
        raise ValueError("BOT_TOKEN is not set in environment")
    if not admin_id:
        raise ValueError("ADMIN_ID is not set in environment")

    return Settings(
        bot_token=token,
        admin_id=int(admin_id),
    )
