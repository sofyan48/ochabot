import logging
import re

# Define a custom filter to extract 'status' from message
class StatusFilter(logging.Filter):
    def filter(self, record):
        # Regular expression to extract status code (like 500, 404, etc.) from the log message
        match = re.search(r'(\d{3})$', record.getMessage())
        if match:
            record.status = match.group(1)
        else:
            record.status = 'N/A'  # Default if no status found
        return True
    

logging_config = logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(status)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "DEBUG",
            "filters": ["status_filter"]
        }
    },
    "filters": {
        "status_filter": {
            "()": StatusFilter
        }
    },
    "loggers": {
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        }
    }
})