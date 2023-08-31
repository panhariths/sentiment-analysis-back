import os

from pydantic_settings import BaseSettings

from .logger.logger_config import get_logging_config

# Define environment variables here
ENV = os.getenv("ENV", "local")
APP_NAME: str = "dummy_users-fastapi-app"
LOGGER_NAME_PREFIX: str = f"{APP_NAME}."
ENV: str = ENV
DEBUG: bool = os.getenv("DEBUG", True)

if DEBUG:
    min_level: str = "DEBUG"
else:
    min_level: str = "INFO"

APP_HOST: str = "0.0.0.0"
APP_PORT: int = 8000

DEFAULT_PAGE_SIZE: str = os.getenv("PAGE_SIZE", "100")
MAX_PAGE_SIZE: str = os.getenv("MAX_PAGE_SIZE", "200")

# Database configs
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_boilerplate")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "boilerplate_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "boilerplate_pass")
POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


class Config(BaseSettings):
    app_name: str = APP_NAME
    app_host: str = APP_HOST
    app_port: int = APP_PORT
    env: str = ENV
    logger_name_prefix: str = LOGGER_NAME_PREFIX
    logging_config: dict = get_logging_config(min_level=min_level, app_name=APP_NAME)
    default_page_size: int = DEFAULT_PAGE_SIZE
    max_page_size: int = MAX_PAGE_SIZE


class DevelopmentConfig(Config):
    # Define environment specific variables here
    pass


class LocalConfig(Config):
    # Define environment specific variables here
    pass


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    env = ENV
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
