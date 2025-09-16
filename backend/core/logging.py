import logging
from logging.config import dictConfig


class LogConfig:
    """Logging configuration to be set for the server"""

    VERSION = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d",
        },
    }
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "logs/app.log",
        },
    }
    loggers = {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "app_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    }


# Apply logging configuration
def setup_logging():
    dictConfig(LogConfig.__dict__)


# Example usage
logger = logging.getLogger("app_logger")
