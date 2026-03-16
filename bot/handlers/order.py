from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.database.models import Cart, CartItem, Order, OrderItem
from bot.keyboards.reply import main_menu_kb
from bot.utils.texts import (
    NO_ORDERS,
    ORDER_CREATED,
    ORDER_EMPTY_CART,
    ORDER_HISTORY_TITLE,
    ORDER_ITEM_LINE,
    ORDER_SUMMARY,
)

order_router = Router()


@order_router.callback_query(F.data == "confirm_order")
async def cb_confirm_order(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id

    result = await session.execute(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = result.scalar_one_or_none()

    if not cart or not cart.items:
        await callback.answer(ORDER_EMPTY_CART, show_alert=True)
        return

    total = sum(item.product.price * item.quantity for item in cart.items)

    order = Order(user_id=user_id, total=total, status="pending")
    session.add(order)
    await session.flush()

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        )
        session.add(order_item)

    for item in cart.items:
        await session.delete(item)

    await session.commit()

    await callback.message.edit_text(
        ORDER_CREATED.format(order_id=order.id, total=total, status=order.status),
        parse_mode="HTML",
    )
    await callback.answer()


@order_router.message(Command("orders"))
@order_router.message(F.text == "📦 My Orders")
async def cmd_orders(message: Message, session: AsyncSession):
    result = await session.execute(
        select(Order)
        .where(Order.user_id == message.from_user.id)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
        .limit(10)
    )
    orders = result.scalars().all()

    if not orders:
        await message.answer(NO_ORDERS)
        return

    text = ORDER_HISTORY_TITLE
    for order in orders:
        items_text = ""
        for oi in order.items:
            items_text += ORDER_ITEM_LINE.format(
                name=oi.product_name,
                qty=oi.quantity,
                subtotal=oi.price * oi.quantity,
            )
        text += ORDER_SUMMARY.format(
            order_id=order.id,
            date=order.created_at.strftime("%Y-%m-%d %H:%M") if order.created_at else "—",
            status=order.status,
            items=items_text,
            total=order.total,
        )

    await message.answer(text, parse_mode="HTML")
