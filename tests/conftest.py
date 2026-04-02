import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.database.models import Base, Cart, CartItem, Category, Product


@pytest_asyncio.fixture
async def engine():
    eng = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest_asyncio.fixture
async def session(engine):
    maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as s:
        yield s


@pytest_asyncio.fixture
async def sample_category(session):
    cat = Category(name="Electronics")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def sample_product(session, sample_category):
    prod = Product(
        name="Wireless Mouse",
        description="Bluetooth mouse",
        price=29.99,
        category_id=sample_category.id,
    )
    session.add(prod)
    await session.commit()
    await session.refresh(prod)
    return prod


@pytest_asyncio.fixture
async def sample_cart(session, sample_product):
    cart = Cart(user_id=123456789)
    session.add(cart)
    await session.flush()

    item = CartItem(cart_id=cart.id, product_id=sample_product.id, quantity=2)
    session.add(item)
    await session.commit()
    await session.refresh(cart)
    return cart
