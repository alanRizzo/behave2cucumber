import logging
from pathlib import Path

from constants import NAME


def setup_logging(
    log_level: int = logging.WARNING, log_dir: str = "./"
) -> logging.Logger:
    """Set up and configure logging with both file and console handlers.

    Args:
        log_level: Logging level to use
        log_dir: Directory to store log files

    Returns:
        Configured logger instance
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-10.10s]  %(message)s"
    )
    shortFormatter = logging.Formatter("[%(levelname)-8.8s]  %(message)s")

    log = logging.getLogger(NAME)
    log.setLevel(log_level)

    # Clear existing handlers if any
    if log.handlers:
        log.handlers.clear()

    # File handler
    file_path = log_path / f"{NAME}.log"
    fileHandler = logging.FileHandler(file_path)
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)

    # Console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(shortFormatter)
    log.addHandler(consoleHandler)

    return log
