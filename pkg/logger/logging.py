import logging
import json
from pkg import utils


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "time": self.formatTime(record, self.datefmt),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "event": utils.json_serializable(record.args),
        }
        # Menambahkan 'extra' jika ada
        if record.__dict__.get('extra'):
            log_record.update(record.__dict__['extra'])
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def configure_logger(logger_name="app_logger", level=logging.DEBUG):
    # Configure the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Attach the JSON formatter
    json_formatter = JsonFormatter()
    console_handler.setFormatter(json_formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)
    
    return logger


logger = configure_logger()