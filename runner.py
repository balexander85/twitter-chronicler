import sys

from filelock import FileLock, Timeout

from chronicler import run_chronicler
from _logger import LOGGER

script_timeout = 10


try:
    with FileLock(f"{__file__}.lock", timeout=script_timeout) as lock:
        run_chronicler()
except Timeout:
    LOGGER.info(
        f"Another instance of this application currently holds the lock. "
        f"(timeout={script_timeout})"
    )
    sys.exit()
