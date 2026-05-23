import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler(sys.stdout)
    # Using JSON format for structured logging
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    logHandler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if not logger.handlers:
        logger.addHandler(logHandler)

    return logger


logger = logging.getLogger("closira")
