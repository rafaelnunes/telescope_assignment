from core.config import settings
from sqlalchemy.ext.asyncio import (  # type: ignore
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession


def get_engine():
    engine = create_async_engine(
        settings.POSTGRES_URL,
        echo=settings.DEBUG,
    )
    return engine


def get_session_maker():
    engine = get_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


async def get_session():
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
