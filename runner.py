import sys

from filelock import FileLock, Timeout

from chronicler import run_chronicler
from _logger import LOGGER

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
    main()
