import logging
from pathlib import Path

from pepyno.constants import NAME


def setup_logging(log_level: int = logging.WARNING, log_dir: str = "./") -> logging.Logger:
    """Set up and configure logging with both file and console handlers.

    Args:
        log_level: Logging level to use
        log_dir: Directory to store log files

    Returns:
        Configured logger instance
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-10.10s]  %(message)s"
    )
    short_formatter = logging.Formatter("[%(levelname)-8.8s]  %(message)s")

    log = logging.getLogger(NAME)
    log.setLevel(log_level)

    if log.handlers:
        log.handlers.clear()

    # File handler
    file_path = log_path / f"{NAME}.log"
    file_handler = logging.FileHandler(file_path)
    file_handler.setFormatter(log_formatter)
    log.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(short_formatter)
    log.addHandler(console_handler)

    return log
