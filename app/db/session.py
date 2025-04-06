from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine() -> Engine:
    engine = create_engine(
        settings.POSTGRES_URL,
        echo=settings.DEBUG,
    )
    return engine


def get_session_maker() -> sessionmaker:
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    SessionLocal = get_session_maker()
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
