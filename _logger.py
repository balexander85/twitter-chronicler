from logging.handlers import TimedRotatingFileHandler
import logging
import os
import sys

MODULE_DIR_PATH = os.path.dirname(__file__)
LOG_DIR_PATH = os.path.join(MODULE_DIR_PATH, "logs")

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
