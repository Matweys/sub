# database/init_models.py
from .db import engine, Base

# ВАЖНО: импортируем модели, чтобы SQLAlchemy их увидела
from products.models import Product, Event


async def init_models() -> None:
    """Создание таблиц по ORM моделям."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("📌 Tables created.")
