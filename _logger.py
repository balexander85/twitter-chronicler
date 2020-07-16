from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import logging

MODULE_PATH = Path(__file__).parent
LOG_DIR_PATH = MODULE_PATH.joinpath("logs")
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
VERBOSE_LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def get_module_logger(name):
    """Pass name of module and return logger instance"""
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(VERBOSE_LOGGER_FORMAT)
    # create file handler which logs even debug messages
    file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR_PATH.joinpath(f"{name}.log"),
        when="midnight",
        interval=1,
        backupCount=7,
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


LOGGER = get_module_logger("default_chronicler_logger")
