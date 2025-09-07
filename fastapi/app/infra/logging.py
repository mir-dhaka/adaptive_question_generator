import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os

def setup_logging(log_dir="logs", time_based: bool = False):
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    # Select the appropriate handler
    if time_based:
        handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8", utc=True
        )
        handler.suffix = "%Y-%m-%d"
    else:
        handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)

    # Avoid adding multiple handlers on reload (e.g. during tests or dev hot reload)
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)
