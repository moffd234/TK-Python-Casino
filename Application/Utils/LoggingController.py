import logging
import os
from logging import FileHandler, Formatter, basicConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("Application")))
PARENT_DIR = os.path.join(BASE_DIR, "logs")


def setup_logging() -> None:
    """
    Configures application-wide logging.

    This sets up log directories, formatters, handlers, and attaches handlers
    to named loggers such as 'account.auth', 'database', and the default root logger.
    """
    os.makedirs(PARENT_DIR, exist_ok=True)

    formatter: Formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    default_file_handler: FileHandler = FileHandler(os.path.join(PARENT_DIR, "app.log"))
    default_file_handler.setFormatter(formatter)
    default_file_handler.setLevel(logging.DEBUG)

    basicConfig(level=logging.INFO, handlers=[default_file_handler])  # Set default logging to use file_handler

    auth_handler: FileHandler = FileHandler(os.path.join(PARENT_DIR, "account.log"))
    auth_handler.setLevel(logging.DEBUG)
    auth_handler.setFormatter(formatter)

    db_handler: FileHandler = FileHandler(os.path.join(PARENT_DIR, "database.log"))
    db_handler.setLevel(logging.DEBUG)
    db_handler.setFormatter(formatter)

    auth_logger = logging.getLogger("account.auth")
    auth_logger.addHandler(auth_handler)
    auth_logger.setLevel(logging.INFO)
    auth_logger.propagate = False

    db_logger = logging.getLogger("database")
    db_logger.addHandler(db_handler)
    db_logger.setLevel(logging.INFO)
    db_logger.propagate = False