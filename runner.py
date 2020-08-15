import sys
import time

from filelock import FileLock, Timeout

from chronicler import run_chronicler
from _logger import get_module_logger

LOGGER = get_module_logger(__name__)
SCRIPT_TIMEOUT = 10


def main():
    try:
        with FileLock(f"{__file__}.lock", timeout=SCRIPT_TIMEOUT):
            run_chronicler()
    except Timeout:
        LOGGER.info(
            f"Another instance of this application currently holds the lock. "
            f"(timeout={SCRIPT_TIMEOUT})"
        )
        sys.exit()


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start_time
    LOGGER.info(f"{__file__} executed in {elapsed:0.2f} seconds.")
