import logging
from logging import config as l_config

import uvicorn

from config.config import config

l_config.dictConfig(config.logging_config)

logger = logging.getLogger(config.logger_name_prefix + __name__)


def main():
    logger.info("Starting uvicorn server...")
    uvicorn.run(
        app="app.server:app",
        host=config.app_host,
        port=config.app_port,
        reload=True if config.env != "production" else False,
        workers=1,
    )

# this is the main function 
if __name__ == "__main__":
    main()
