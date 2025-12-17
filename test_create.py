# test_create.py
import asyncio

from database.db import async_session_maker
from products.models import Product, Event, EventType
from datetime import datetime


async def create_one_product():
    # 1. создаём сессию
    async with async_session_maker() as session:
        # 2. создаём ORM-объект (пока только в памяти, НЕ в базе)
        new_product = Product(
            name="Test Product",
            price=99.99,
            category="education",
            owner="matwey",
        )

        print("👉 Создали объект (ещё НЕ в базе):", new_product)

        # 3. добавляем в сессию
        session.add(new_product)

        # 4. сохраняем изменения в базе
        await session.commit()

        # 5. обновляем объект из базы (получим id и др. значения)
        await session.refresh(new_product)

        print("✅ Объект сохранён в БД. ID:", new_product.id)


async def create_one_event():
    async with async_session_maker() as session:
        new_event = Event(
            title="Test Webinar",
            description="Учебный ивент по CRUD",
            event_type=EventType.online,
            start_at=datetime.utcnow(),
            end_at=None,
            capacity=100,
            price=0,
        )

        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)

        print("✅ Event сохранён в БД. ID:", new_event.id)


async def main():
    await create_one_product()
    await create_one_event()


if __name__ == "__main__":
    asyncio.run(main())
