from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from SHWEBS.config import settings
from SHWEBS.models import Base
"""Файл для соединения с БД"""


engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
)


async_session = sessionmaker(engine,
                             class_=AsyncSession,
                             expire_on_commit=False,
                             )


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
