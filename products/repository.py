# products/repository.py
from typing import cast
from sqlalchemy import select
from products.exceptions import ProductCreateError, ProductGetAllError, ProductGetOwnerError
from products.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from products.schemas import CreateProducts


async def add_product(items: CreateProducts, db: AsyncSession) -> Product:
    new_item = Product(
        name=items.name,
        price=items.price,
        category=items.category,
        owner=items.owner,
    )
    db.add(new_item)

    await db.flush()
    await db.refresh(new_item)
    return new_item


async def select_all_products(db: AsyncSession) -> list[Product]:
    stmt = select(Product)
    try:
        result = await db.execute(stmt)
    except Exception as err:
        raise ProductGetAllError("Ошибка при получении данных") from err

    return cast(list[Product], result.scalars().all())


async def select_products_by_owner(db: AsyncSession, owner: str) -> list[Product]:
    stmt = select(Product).where(Product.owner == owner)
    try:
        result = await db.execute(stmt)
    except Exception as err:
        raise ProductGetOwnerError("Не удалось получить продукт") from err

    return cast(list[Product], result.scalars().all())
