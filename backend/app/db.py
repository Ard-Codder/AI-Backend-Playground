"""
Настройка базы данных
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (  # type: ignore
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase  # type: ignore

from .config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    pass


# Создание асинхронного движка
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        # Создание всех таблиц
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Закрытие соединения с базой данных"""
    await engine.dispose()
