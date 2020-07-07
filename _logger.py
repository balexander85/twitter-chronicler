from logging.handlers import TimedRotatingFileHandler
import logging
import os


MODULE_DIR_PATH = os.path.dirname(__file__)
LOG_DIR_PATH = os.path.join(MODULE_DIR_PATH, "logs")
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
VERBOSE_LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def get_module_logger(name):
    """Pass name of module and return logger instance"""
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(VERBOSE_LOGGER_FORMAT)
    # create file handler which logs even debug messages
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR_PATH, f"{name}.log"),
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


LOGGER = logging.getLogger("twitter_chronicler")
LOGGER.setLevel(logging.INFO)

# create formatter and add it to the handlers
logger_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
formatter = logging.Formatter(logger_format)

# create file handler which logs even debug messages
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR_PATH, "chronicler.log"), when="midnight", interval=1
)
file_handler.suffix = "%Y-%m-%d"
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# add the handlers to the logger
LOGGER.addHandler(file_handler)
LOGGER.addHandler(console_handler)
