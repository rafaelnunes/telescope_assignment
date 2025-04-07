from typing import AsyncGenerator

from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine  # type: ignore
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


def get_engine():
    engine = create_async_engine(
        settings.POSTGRES_URL,
        echo=settings.DEBUG,
    )
    return engine


def get_session_maker():
    engine = get_engine()
    return sessionmaker(
        engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_session_maker()
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
