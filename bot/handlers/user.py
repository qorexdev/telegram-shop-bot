from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.database.models import Cart, CartItem, Category, Product
from bot.keyboards.inline import categories_kb, product_detail_kb, products_kb
from bot.keyboards.reply import main_menu_kb
from bot.utils.texts import (
    ADDED_TO_CART,
    ALREADY_OUT_OF_STOCK,
    CATALOG_EMPTY,
    CATEGORIES_TITLE,
    HELP,
    IN_STOCK,
    OUT_OF_STOCK,
    PRODUCT_CARD,
    PRODUCT_NOT_FOUND,
    PRODUCTS_TITLE,
    SEARCH_NO_RESULTS,
    SEARCH_PROMPT,
    SEARCH_RESULTS,
    SEARCH_TOO_SHORT,
    WELCOME,
)

user_router = Router()


class SearchState(StatesGroup):
    waiting_query = State()


@user_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_menu_kb())


@user_router.message(Command("help"))
@user_router.message(F.text == "ℹ️ Help")
async def cmd_help(message: Message):
    await message.answer(HELP)


@user_router.message(Command("search"))
@user_router.message(F.text == "🔍 Search")
async def cmd_search(message: Message, state: FSMContext, session: AsyncSession, command: CommandObject = None):
    # /search <query> — search immediately
    if command and command.args and len(command.args.strip()) >= 2:
        await _do_search(message, command.args.strip(), session)
        return
    await state.set_state(SearchState.waiting_query)
    await message.answer(SEARCH_PROMPT)


@user_router.message(SearchState.waiting_query)
async def handle_search_query(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    query = message.text.strip() if message.text else ""
    if len(query) < 2:
        await message.answer(SEARCH_TOO_SHORT)
        return
    await _do_search(message, query, session)


async def _do_search(message: Message, query: str, session: AsyncSession):
    result = await session.execute(
        select(Product).where(Product.in_stock == True, Product.name.ilike(f"%{query}%"))
    )
    products = result.scalars().all()
    if not products:
        await message.answer(SEARCH_NO_RESULTS.format(query=query))
        return
    await message.answer(
        SEARCH_RESULTS.format(count=len(products), query=query),
        reply_markup=products_kb(products),
    )


@user_router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "🛠 Developed by qorex\n\n"
        '📱 Telegram: <a href="https://t.me/qorexdev">@qorexdev</a>\n'
        '💻 GitHub: <a href="https://github.com/qorexdev">github.com/qorexdev</a>'
    )


@user_router.message(Command("catalog"))
@user_router.message(F.text == "🛍 Catalog")
async def cmd_catalog(message: Message, session: AsyncSession):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await message.answer(CATALOG_EMPTY)
        return
    await message.answer(CATEGORIES_TITLE, reply_markup=categories_kb(categories))


@user_router.callback_query(F.data == "back_to_categories")
async def cb_back_to_categories(callback: CallbackQuery, session: AsyncSession):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await callback.message.edit_text(CATALOG_EMPTY)
    else:
        await callback.message.edit_text(CATEGORIES_TITLE, reply_markup=categories_kb(categories))
    await callback.answer()


@user_router.callback_query(F.data.startswith("category:"))
async def cb_category(callback: CallbackQuery, session: AsyncSession):
    category_id = int(callback.data.split(":")[1])
    result = await session.execute(
        select(Product).where(Product.category_id == category_id, Product.in_stock == True)
    )
    products = result.scalars().all()

    cat_result = await session.execute(select(Category).where(Category.id == category_id))
    category = cat_result.scalar_one_or_none()
    cat_name = category.name if category else "Unknown"

    if not products:
        await callback.message.edit_text(
            PRODUCTS_TITLE.format(category=cat_name) + "\n\nNo products available.",
            reply_markup=categories_kb(
                (await session.execute(select(Category))).scalars().all()
            ),
        )
    else:
        await callback.message.edit_text(
            PRODUCTS_TITLE.format(category=cat_name),
            reply_markup=products_kb(products),
        )
    await callback.answer()


@user_router.callback_query(F.data.startswith("product:"))
async def cb_product(callback: CallbackQuery, session: AsyncSession):
    product_id = int(callback.data.split(":")[1])
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        await callback.answer(PRODUCT_NOT_FOUND, show_alert=True)
        return

    stock_status = IN_STOCK if product.in_stock else OUT_OF_STOCK
    text = PRODUCT_CARD.format(
        name=product.name,
        description=product.description or "No description",
        price=product.price,
        stock_status=stock_status,
    )

    if product.image_url:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=product.image_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=product_detail_kb(product),
        )
    else:
        await callback.message.edit_text(
            text, parse_mode="HTML", reply_markup=product_detail_kb(product)
        )
    await callback.answer()


@user_router.callback_query(F.data.startswith("add_to_cart:"))
async def cb_add_to_cart(callback: CallbackQuery, session: AsyncSession):
    product_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    product = await session.get(Product, product_id)
    if not product or not product.in_stock:
        await callback.answer(ALREADY_OUT_OF_STOCK, show_alert=True)
        return

    result = await session.execute(
        select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.items))
    )
    cart = result.scalar_one_or_none()

    if not cart:
        cart = Cart(user_id=user_id)
        session.add(cart)
        await session.flush()

    existing_item = next((item for item in cart.items if item.product_id == product_id), None)
    if existing_item:
        existing_item.quantity += 1
    else:
        cart.items.append(CartItem(cart_id=cart.id, product_id=product_id, quantity=1))

    await session.commit()
    await callback.answer(ADDED_TO_CART.format(product=product.name), show_alert=True)
