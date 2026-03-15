import logging
import os
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


class LoggerManager:
    """Centralized logging manager for PyMessenger."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self.logger = logging.getLogger("PyMessenger")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            # File handler
            file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def log_login(self, username: str):
        self.info(f"USER LOGIN  : '{username}' logged in successfully.")

    def log_register(self, username: str):
        self.info(f"USER REGISTER: '{username}' registered successfully.")

    def log_message_sent(self, sender: str, receiver: str):
        self.info(f"MESSAGE SENT : '{sender}' → '{receiver}'")

    def log_error(self, context: str, error: Exception):
        self.error(f"ERROR in {context}: {type(error).__name__} - {error}")
