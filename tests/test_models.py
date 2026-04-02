import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.database.models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
)

pytestmark = pytest.mark.asyncio


async def test_create_category(session):
    cat = Category(name="Books")
    session.add(cat)
    await session.commit()

    res = await session.execute(select(Category).where(Category.name == "Books"))
    assert res.scalar_one().id is not None


async def test_category_repr(sample_category):
    r = repr(sample_category)
    assert "Electronics" in r
    assert "Category" in r


async def test_create_product(session, sample_category):
    p = Product(name="Keyboard", price=49.99, category_id=sample_category.id)
    session.add(p)
    await session.commit()

    res = await session.execute(select(Product).where(Product.name == "Keyboard"))
    row = res.scalar_one()
    assert row.price == 49.99
    assert row.in_stock is True


async def test_product_repr(sample_product):
    r = repr(sample_product)
    assert "Wireless Mouse" in r
    assert "29.99" in r


async def test_product_default_description(session, sample_category):
    p = Product(name="USB Cable", price=5.0, category_id=sample_category.id)
    session.add(p)
    await session.commit()
    await session.refresh(p)
    assert p.description == ""


async def test_product_belongs_to_category(session, sample_product, sample_category):
    res = await session.execute(
        select(Product)
        .where(Product.id == sample_product.id)
        .options(selectinload(Product.category))
    )
    prod = res.scalar_one()
    assert prod.category.name == "Electronics"


async def test_category_products_relationship(session, sample_category):
    for name, price in [("Mouse", 19.99), ("Monitor", 299.0)]:
        session.add(Product(name=name, price=price, category_id=sample_category.id))
    await session.commit()

    res = await session.execute(
        select(Category)
        .where(Category.id == sample_category.id)
        .options(selectinload(Category.products))
    )
    cat = res.scalar_one()
    assert len(cat.products) >= 2


async def test_cascade_delete_category(session, sample_category):
    p = Product(name="Tablet", price=199.0, category_id=sample_category.id)
    session.add(p)
    await session.commit()
    pid = p.id

    await session.delete(sample_category)
    await session.commit()

    res = await session.execute(select(Product).where(Product.id == pid))
    assert res.scalar_one_or_none() is None


async def test_create_cart(session):
    cart = Cart(user_id=999)
    session.add(cart)
    await session.commit()
    assert cart.id is not None
    assert cart.user_id == 999


async def test_add_item_to_cart(session, sample_cart, sample_product):
    res = await session.execute(
        select(Cart)
        .where(Cart.id == sample_cart.id)
        .options(selectinload(Cart.items))
    )
    cart = res.scalar_one()
    assert len(cart.items) == 1
    assert cart.items[0].product_id == sample_product.id
    assert cart.items[0].quantity == 2


async def test_update_cart_item_quantity(session, sample_cart):
    res = await session.execute(
        select(CartItem).where(CartItem.cart_id == sample_cart.id)
    )
    item = res.scalar_one()
    item.quantity = 5
    await session.commit()
    await session.refresh(item)
    assert item.quantity == 5


async def test_remove_cart_item(session, sample_cart):
    res = await session.execute(
        select(CartItem).where(CartItem.cart_id == sample_cart.id)
    )
    item = res.scalar_one()
    await session.delete(item)
    await session.commit()

    res = await session.execute(
        select(CartItem).where(CartItem.cart_id == sample_cart.id)
    )
    assert res.scalar_one_or_none() is None


async def test_cascade_delete_cart(session, sample_cart):
    cart_id = sample_cart.id
    await session.delete(sample_cart)
    await session.commit()

    res = await session.execute(select(CartItem).where(CartItem.cart_id == cart_id))
    assert res.scalars().all() == []


async def test_create_order(session):
    order = Order(user_id=123, total=59.98, status="pending")
    session.add(order)
    await session.commit()
    assert order.id is not None
    assert order.status == "pending"


async def test_order_with_items(session, sample_product):
    order = Order(user_id=123, total=59.98)
    session.add(order)
    await session.flush()

    oi = OrderItem(
        order_id=order.id,
        product_id=sample_product.id,
        product_name=sample_product.name,
        price=sample_product.price,
        quantity=2,
    )
    session.add(oi)
    await session.commit()

    res = await session.execute(
        select(Order).where(Order.id == order.id).options(selectinload(Order.items))
    )
    o = res.scalar_one()
    assert len(o.items) == 1
    assert o.items[0].product_name == "Wireless Mouse"


async def test_order_from_cart(session, sample_cart, sample_product):
    """Simulate what the order handler does: cart -> order -> clear cart."""
    res = await session.execute(
        select(Cart)
        .where(Cart.id == sample_cart.id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = res.scalar_one()

    total = sum(i.product.price * i.quantity for i in cart.items)
    order = Order(user_id=cart.user_id, total=total)
    session.add(order)
    await session.flush()

    for i in cart.items:
        session.add(OrderItem(
            order_id=order.id,
            product_id=i.product_id,
            product_name=i.product.name,
            price=i.product.price,
            quantity=i.quantity,
        ))

    for i in list(cart.items):
        await session.delete(i)

    await session.commit()

    assert order.total == sample_product.price * 2

    res = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    assert res.scalars().all() == []


async def test_cascade_delete_order(session, sample_product):
    order = Order(user_id=555, total=29.99)
    session.add(order)
    await session.flush()

    oi = OrderItem(
        order_id=order.id,
        product_id=sample_product.id,
        product_name="test",
        price=29.99,
        quantity=1,
    )
    session.add(oi)
    await session.commit()

    oid = order.id
    await session.delete(order)
    await session.commit()

    res = await session.execute(select(OrderItem).where(OrderItem.order_id == oid))
    assert res.scalars().all() == []


async def test_multiple_categories(session):
    for name in ["Food", "Clothing", "Tech"]:
        session.add(Category(name=name))
    await session.commit()

    res = await session.execute(select(Category))
    cats = res.scalars().all()
    assert len(cats) >= 3
