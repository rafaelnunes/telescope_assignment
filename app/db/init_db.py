import logging

from db.session import get_session_maker


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def create_init_data() -> None:
    SessionLocal = get_session_maker()
    session = SessionLocal()

    session.add()
    session.add()

    session.commit()


def main() -> None:
    logger.info("Creating initial data")
    create_init_data()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
