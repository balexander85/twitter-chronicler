import logging
import os

MODULE_DIR_PATH = os.path.dirname(__file__)
LOG_DIR_PATH = os.path.join(MODULE_DIR_PATH, "logs")

LOGGER = logging.getLogger("twitter_chronicler")
LOGGER.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# create file handler which logs even debug messages
file_handler = logging.FileHandler(os.path.join(LOG_DIR_PATH, "chronicler.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

# add the handlers to the logger
LOGGER.addHandler(console_handler)
LOGGER.addHandler(file_handler)
