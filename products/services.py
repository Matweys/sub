# products/services.py
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from products.models import Product
from products.outbox_model import OutboxEvent
from products.repository import add_product, select_all_products, select_products_by_owner
from products.exceptions import PermissionDenied, ProductCreateError
from products.schemas import CreateProducts


def utcnow():
    return datetime.now(timezone.utc)


async def create_product(user: dict, items: CreateProducts, db: AsyncSession) -> Product:
    if user.get("role") != "admin":
        raise PermissionDenied("Нет доступа на добавление продукта")

    try:
        async with db.begin():
            product = await add_product(items, db)

            db.add(
                OutboxEvent(
                    topic="product-events",
                    key=str(product.id),
                    event_type="ProductCreated",
                    aggregate_type="product",
                    aggregate_id=str(product.id),
                    payload={
                        "event": "ProductCreated",
                        "product": {
                            "id": product.id,
                            "name": product.name,
                            "price": float(product.price),
                            "category": product.category,
                            "owner": product.owner,
                        },
                    },
                    status="pending",
                    attempts=0,
                    available_at=utcnow(),
                )
            )

        return product

    except Exception as err:
        raise ProductCreateError("Ошибка при создании продукта (product + outbox)") from err


async def get_all_products(user: dict, db: AsyncSession) -> list[Product]:
    if user.get("role") != "admin":
        raise PermissionDenied("Нет доступа на просмотр/получение данных")

    return await select_all_products(db)


async def get_products_by_owner(db: AsyncSession, owner: str) -> list[Product]:
    return await select_products_by_owner(db, owner)

