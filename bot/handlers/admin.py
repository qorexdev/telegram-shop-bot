from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import get_settings
from bot.database.models import Category, Product
from bot.keyboards.inline import admin_categories_kb, admin_products_kb
from bot.keyboards.reply import admin_menu_kb, main_menu_kb
from bot.utils.texts import (
    ADMIN_ADD_CATEGORY,
    ADMIN_CATEGORY_ADDED,
    ADMIN_CATEGORY_DELETED,
    ADMIN_DELETE_CATEGORY,
    ADMIN_ENTER_DESC,
    ADMIN_ENTER_IMAGE,
    ADMIN_ENTER_NAME,
    ADMIN_ENTER_PRICE,
    ADMIN_INVALID_PRICE,
    ADMIN_ONLY,
    ADMIN_PANEL,
    ADMIN_PRODUCT_ADDED,
    ADMIN_PRODUCT_DELETED,
    ADMIN_PRODUCTS_EMPTY,
    ADMIN_SELECT_CATEGORY,
    ADMIN_SELECT_PRODUCT,
    ADMIN_STOCK_TOGGLED,
    ADMIN_TOGGLE_STOCK,
    IN_STOCK,
    OUT_OF_STOCK,
)

admin_router = Router()
settings = get_settings()


class AddProduct(StatesGroup):
    category_id = State()
    name = State()
    description = State()
    price = State()
    image_url = State()


class AddCategory(StatesGroup):
    name = State()


def is_admin(user_id: int) -> bool:
    return user_id == settings.admin_id


@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer(ADMIN_ONLY)
        return
    await message.answer(ADMIN_PANEL, reply_markup=admin_menu_kb())


@admin_router.message(F.text == "🔙 Back to Menu")
async def cmd_back_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Main menu", reply_markup=main_menu_kb())


# --- Add Category ---

@admin_router.message(F.text == "➕ Add Category")
async def add_category_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddCategory.name)
    await message.answer(ADMIN_ADD_CATEGORY)


@admin_router.message(AddCategory.name)
async def add_category_name(message: Message, state: FSMContext, session: AsyncSession):
    category = Category(name=message.text.strip())
    session.add(category)
    await session.commit()
    await state.clear()
    await message.answer(
        ADMIN_CATEGORY_ADDED.format(name=category.name),
        reply_markup=admin_menu_kb(),
    )


# --- Delete Category ---

@admin_router.message(F.text == "🗑 Delete Category")
async def delete_category_start(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await message.answer("No categories to delete.")
        return
    await message.answer(ADMIN_DELETE_CATEGORY, reply_markup=admin_categories_kb(categories, "delete"))


@admin_router.callback_query(F.data.startswith("admin_delete_cat:"))
async def cb_delete_category(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        return
    cat_id = int(callback.data.split(":")[1])
    category = await session.get(Category, cat_id)
    if category:
        await session.delete(category)
        await session.commit()
    await callback.message.edit_text(ADMIN_CATEGORY_DELETED)
    await callback.answer()


# --- Add Product ---

@admin_router.message(F.text == "➕ Add Product")
async def add_product_start(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await message.answer("Create a category first.")
        return
    await message.answer(ADMIN_SELECT_CATEGORY, reply_markup=admin_categories_kb(categories, "addprod"))


@admin_router.callback_query(F.data.startswith("admin_addprod_cat:"))
async def cb_select_category_for_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    cat_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=cat_id)
    await state.set_state(AddProduct.name)
    await callback.message.edit_text(ADMIN_ENTER_NAME)
    await callback.answer()


@admin_router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddProduct.description)
    await message.answer(ADMIN_ENTER_DESC)


@admin_router.message(AddProduct.description)
async def add_product_desc(message: Message, state: FSMContext):
    desc = message.text.strip()
    await state.update_data(description="" if desc == "-" else desc)
    await state.set_state(AddProduct.price)
    await message.answer(ADMIN_ENTER_PRICE)


@admin_router.message(AddProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip())
    except ValueError:
        await message.answer(ADMIN_INVALID_PRICE)
        return
    await state.update_data(price=price)
    await state.set_state(AddProduct.image_url)
    await message.answer(ADMIN_ENTER_IMAGE)


@admin_router.message(AddProduct.image_url)
async def add_product_image(message: Message, state: FSMContext, session: AsyncSession):
    img = message.text.strip()
    data = await state.get_data()

    product = Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image_url=None if img == "-" else img,
        category_id=data["category_id"],
        in_stock=True,
    )
    session.add(product)
    await session.commit()
    await state.clear()
    await message.answer(
        ADMIN_PRODUCT_ADDED.format(name=product.name),
        reply_markup=admin_menu_kb(),
    )


# --- Delete Product ---

@admin_router.message(F.text == "🗑 Delete Product")
async def delete_product_start(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await message.answer("No categories.")
        return
    await message.answer(ADMIN_SELECT_CATEGORY, reply_markup=admin_categories_kb(categories, "delprodcat"))


@admin_router.callback_query(F.data.startswith("admin_delprodcat_cat:"))
async def cb_delete_product_category(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        return
    cat_id = int(callback.data.split(":")[1])
    result = await session.execute(select(Product).where(Product.category_id == cat_id))
    products = result.scalars().all()
    if not products:
        await callback.message.edit_text(ADMIN_PRODUCTS_EMPTY)
        await callback.answer()
        return
    await callback.message.edit_text(ADMIN_SELECT_PRODUCT, reply_markup=admin_products_kb(products, "delete"))
    await callback.answer()


@admin_router.callback_query(F.data.startswith("admin_delete_prod:"))
async def cb_delete_product(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        return
    prod_id = int(callback.data.split(":")[1])
    product = await session.get(Product, prod_id)
    if product:
        await session.delete(product)
        await session.commit()
    await callback.message.edit_text(ADMIN_PRODUCT_DELETED)
    await callback.answer()


# --- Toggle Stock ---

@admin_router.message(F.text == "📦 Toggle Stock")
async def toggle_stock_start(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    if not categories:
        await message.answer("No categories.")
        return
    await message.answer(ADMIN_SELECT_CATEGORY, reply_markup=admin_categories_kb(categories, "stockcat"))


@admin_router.callback_query(F.data.startswith("admin_stockcat_cat:"))
async def cb_stock_category(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        return
    cat_id = int(callback.data.split(":")[1])
    result = await session.execute(select(Product).where(Product.category_id == cat_id))
    products = result.scalars().all()
    if not products:
        await callback.message.edit_text(ADMIN_PRODUCTS_EMPTY)
        await callback.answer()
        return
    await callback.message.edit_text(ADMIN_TOGGLE_STOCK, reply_markup=admin_products_kb(products, "stock"))
    await callback.answer()


@admin_router.callback_query(F.data.startswith("admin_stock_prod:"))
async def cb_toggle_stock(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        return
    prod_id = int(callback.data.split(":")[1])
    product = await session.get(Product, prod_id)
    if product:
        product.in_stock = not product.in_stock
        await session.commit()
        status = IN_STOCK if product.in_stock else OUT_OF_STOCK
        await callback.message.edit_text(ADMIN_STOCK_TOGGLED.format(name=product.name, status=status))
    await callback.answer()
