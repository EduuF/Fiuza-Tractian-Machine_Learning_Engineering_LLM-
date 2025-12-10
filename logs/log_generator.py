"""Custom logs generator."""

import logging
import sys
from typing import Literal

from colorama import Fore, Style, init

LogLevel = Literal["info", "warning", "error", "debug"]


init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom logging formatter to add colors based on log level."""

    # Color mapping
    _COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record injecting ANSI color codes."""

        # Determine color
        color = self._COLORS.get(record.levelno, Fore.WHITE)

        # Format: [TIMESTAMP] [LEVEL] Message
        log_fmt = f"{Fore.LIGHTBLACK_EX}%(asctime)s{Style.RESET_ALL} | {color}%(levelname)-8s{Style.RESET_ALL} | %(message)s"

        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(name: str = "TractianApp") -> logging.Logger:
    """Configures and returns a singleton logger instance with the custom formatter."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter())

        logger.addHandler(handler)

        logger.propagate = False

    return logger


_logger = setup_logger()


def log_message(message: str, level: LogLevel = "info") -> None:
    """
    Logs a message with the specified severity level using the colored logger.

    Args:
        message (str): The content to log.
        level (str): The severity level ('info', 'warning', 'error', 'debug').
    """
    level_lower = level.lower()

    if level_lower == "info":
        _logger.info(message)
    elif level_lower == "warning":
        _logger.warning(message)
    elif level_lower == "error":
        _logger.error(message)
    elif level_lower == "debug":
        _logger.debug(message)
    else:
        # Fallback for unknown levels
        _logger.info(f"[UNKNOWN LEVEL: {level}] {message}")
