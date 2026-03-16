from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models import Category, Product


def categories_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.add(InlineKeyboardButton(text=cat.name, callback_data=f"category:{cat.id}"))
    builder.adjust(2)
    return builder.as_markup()


def products_kb(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in products:
        label = f"{p.name} — ${p.price:.2f}"
        builder.add(InlineKeyboardButton(text=label, callback_data=f"product:{p.id}"))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Back to categories", callback_data="back_to_categories"))
    return builder.as_markup()


def product_detail_kb(product: Product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if product.in_stock:
        builder.add(InlineKeyboardButton(text="🛒 Add to cart", callback_data=f"add_to_cart:{product.id}"))
    builder.add(
        InlineKeyboardButton(text="🔙 Back", callback_data=f"category:{product.category_id}")
    )
    builder.adjust(1)
    return builder.as_markup()


def cart_kb(items: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.row(
            InlineKeyboardButton(text=f"❌ {item.product.name}", callback_data=f"cart_remove:{item.id}"),
            InlineKeyboardButton(text="➖", callback_data=f"cart_minus:{item.id}"),
            InlineKeyboardButton(text=str(item.quantity), callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_plus:{item.id}"),
        )
    builder.row(InlineKeyboardButton(text="✅ Checkout", callback_data="checkout"))
    return builder.as_markup()


def confirm_order_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_order"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_order"),
    )
    return builder.as_markup()


# --- Admin keyboards ---

def admin_categories_kb(categories: list[Category], action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.add(InlineKeyboardButton(text=cat.name, callback_data=f"admin_{action}_cat:{cat.id}"))
    builder.adjust(2)
    return builder.as_markup()


def admin_products_kb(products: list[Product], action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in products:
        builder.add(InlineKeyboardButton(text=p.name, callback_data=f"admin_{action}_prod:{p.id}"))
    builder.adjust(1)
    return builder.as_markup()
