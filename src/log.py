import logging
import os

logger = logging.getLogger("stargazer")


def configure_logging() -> None:
    logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s] %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
