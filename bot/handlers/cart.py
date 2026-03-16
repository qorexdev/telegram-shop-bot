from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.database.models import Cart, CartItem
from bot.keyboards.inline import cart_kb, confirm_order_kb
from bot.utils.texts import (
    CART_EMPTY,
    CART_ITEM,
    CART_TITLE,
    CART_TOTAL,
    CONFIRM_ORDER,
    ITEM_REMOVED,
    QUANTITY_UPDATED,
)

cart_router = Router()


async def _get_cart_text_and_items(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = result.scalar_one_or_none()

    if not cart or not cart.items:
        return None, None, 0

    text = CART_TITLE
    total = 0.0
    for i, item in enumerate(cart.items, 1):
        subtotal = item.product.price * item.quantity
        total += subtotal
        text += CART_ITEM.format(
            i=i,
            name=item.product.name,
            price=item.product.price,
            qty=item.quantity,
            subtotal=subtotal,
        )
    text += CART_TOTAL.format(total=total)
    return text, cart.items, total


@cart_router.message(Command("cart"))
@cart_router.message(F.text == "🛒 Cart")
async def cmd_cart(message: Message, session: AsyncSession):
    text, items, total = await _get_cart_text_and_items(session, message.from_user.id)
    if not text:
        await message.answer(CART_EMPTY)
        return
    await message.answer(text, parse_mode="HTML", reply_markup=cart_kb(items))


@cart_router.callback_query(F.data.startswith("cart_remove:"))
async def cb_cart_remove(callback: CallbackQuery, session: AsyncSession):
    item_id = int(callback.data.split(":")[1])
    item = await session.get(CartItem, item_id)
    if item:
        await session.delete(item)
        await session.commit()
    await callback.answer(ITEM_REMOVED)
    await _refresh_cart(callback, session)


@cart_router.callback_query(F.data.startswith("cart_plus:"))
async def cb_cart_plus(callback: CallbackQuery, session: AsyncSession):
    item_id = int(callback.data.split(":")[1])
    item = await session.get(CartItem, item_id)
    if item:
        item.quantity += 1
        await session.commit()
    await callback.answer(QUANTITY_UPDATED)
    await _refresh_cart(callback, session)


@cart_router.callback_query(F.data.startswith("cart_minus:"))
async def cb_cart_minus(callback: CallbackQuery, session: AsyncSession):
    item_id = int(callback.data.split(":")[1])
    item = await session.get(CartItem, item_id)
    if item:
        if item.quantity > 1:
            item.quantity -= 1
        else:
            await session.delete(item)
        await session.commit()
    await callback.answer(QUANTITY_UPDATED)
    await _refresh_cart(callback, session)


@cart_router.callback_query(F.data == "checkout")
async def cb_checkout(callback: CallbackQuery, session: AsyncSession):
    text, items, total = await _get_cart_text_and_items(session, callback.from_user.id)
    if not text:
        await callback.answer(CART_EMPTY, show_alert=True)
        return
    await callback.message.edit_text(
        CONFIRM_ORDER.format(total=total),
        parse_mode="HTML",
        reply_markup=confirm_order_kb(),
    )
    await callback.answer()


@cart_router.callback_query(F.data == "cancel_order")
async def cb_cancel_order(callback: CallbackQuery, session: AsyncSession):
    text, items, total = await _get_cart_text_and_items(session, callback.from_user.id)
    if not text:
        await callback.message.edit_text(CART_EMPTY)
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=cart_kb(items))
    await callback.answer()


@cart_router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()


async def _refresh_cart(callback: CallbackQuery, session: AsyncSession):
    text, items, total = await _get_cart_text_and_items(session, callback.from_user.id)
    if not text:
        await callback.message.edit_text(CART_EMPTY)
    else:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=cart_kb(items))
