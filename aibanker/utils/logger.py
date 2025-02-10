# aibanker/utils/logger.py

import logging
import sys

def init_logger(level=logging.INFO):
    logger = logging.getLogger()  # root logger
    logger.setLevel(level)

    if logger.handlers:
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add handler to the root logger
    logger.addHandler(console_handler)


def get_logger(name: str = None) -> logging.Logger:
    return logging.getLogger(name)
