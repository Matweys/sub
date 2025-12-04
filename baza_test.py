from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_db"

engine = create_async_engine(DATABASE_URL, echo=True)
