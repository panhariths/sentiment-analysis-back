import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as settings

logger = logging.getLogger(settings.config.logger_name_prefix + __name__)

# Create sqlalchemy engine with postgres database
engine = create_engine(settings.POSTGRES_URL)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
