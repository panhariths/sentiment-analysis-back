import logging

from fastapi import FastAPI

from config.config import config

from .routes import router

logger = logging.getLogger(config.logger_name_prefix + __name__)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router=router, prefix="/api/v1")


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Sentiment Analysis API",
        description="API For Sentiment Analysis Project Demonstration",
        version="1.0.0",
    )
    init_routers(app_=app_)
    return app_


app = create_app()


@app.on_event("startup")
async def startup():
    logger.info("Starting application...")
    # Register functions to run on application startup here
    # await check_connection_with_database()
    # await run_migrations()
    pass


@app.on_event("shutdown")
async def shutdown():
    # Register functions to run on application shutdown here
    logger.info("Shutting down application")
