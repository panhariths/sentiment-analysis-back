import logging
import sys

import structlog

from .log_processors import (
    module_info_processor,
    service_name_processor,
    time_stamp_processor,
)

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

shared_processors = [
    # adding time key through a self defined processor
    time_stamp_processor,
    structlog.stdlib.add_log_level,
    # adding custom keys through a self defined processor
    service_name_processor,
    # adding caller key to include the exact line of logging
    module_info_processor,
    # structlog uses a default key of "event" for all the messages. Replacing the "event" key by "msg" here
    structlog.processors.EventRenamer("msg"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

# structlog is used to configure the logging format to our custom use-cases.
structlog.configure(
    processors=shared_processors
    + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
)


def get_logging_config(min_level=logging.INFO, app_name="default"):
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "time=[%(asctime)s] level=%(levelname)s  service=analytics caller=(%(name)s.%(funcName)s.%(lineno)s) msg=%(message)s "
                "transaction.id=%(elasticapm_transaction_id)s trace.id=%(elasticapm_trace_id)s "
            },
            "simple": {"format": "[%(asctime)s] %(levelname)s - %(message)s"},
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "foreign_pre_chain": shared_processors,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.JSONRenderer(),
                ],
            },
        },
        "handlers": {
            "console": {
                "level": min_level,
                "class": "logging.StreamHandler",
                "formatter": "json_formatter",
            },
        },
        "loggers": {
            app_name: {
                "handlers": ["console"],
                "level": min_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": min_level,
                "propagate": True,
            },
        },
    }
