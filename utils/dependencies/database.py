import logging

from config import config as settings
from datastores.database.postgres.session import SessionLocal

logger = logging.getLogger(settings.config.logger_name_prefix + __name__)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    except Exception as error:
        # if we fail somehow rollback the connection
        logger.exception("Database error, rolling back...")
        logger.exception(error)
        db.rollback()
        raise
    finally:
        db.close()
