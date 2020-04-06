import logging
import os

MODULE_DIR_PATH = os.path.dirname(__file__)
LOG_DIR_PATH = os.path.join(MODULE_DIR_PATH, "logs")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(LOG_DIR_PATH, "chronicler.log"))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
LOGGER.addHandler(fh)
LOGGER.addHandler(ch)
