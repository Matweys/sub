# database/db.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://localhost:5432/fastapi_db"


class Base(DeclarativeBase):
    """Базовый класс для всех ORM моделей."""
    pass


engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # включено для дебага
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency, отдающее асинхронную сессию."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
