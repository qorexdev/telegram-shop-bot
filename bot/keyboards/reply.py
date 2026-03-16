from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Catalog"), KeyboardButton(text="🛒 Cart")],
            [KeyboardButton(text="📦 My Orders"), KeyboardButton(text="ℹ️ Help")],
        ],
        resize_keyboard=True,
    )


def admin_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add Category"), KeyboardButton(text="➕ Add Product")],
            [KeyboardButton(text="🗑 Delete Category"), KeyboardButton(text="🗑 Delete Product")],
            [KeyboardButton(text="📦 Toggle Stock"), KeyboardButton(text="🔙 Back to Menu")],
        ],
        resize_keyboard=True,
    )
