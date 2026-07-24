import logging
import sys

from styleai.config import Config


def setup_logging():
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)

    logger = logging.getLogger("styleai")
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [styleai] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
