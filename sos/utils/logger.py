"""
Logging utilities for SOS (SKA Observation Simulator).

Provides centralized logging configuration with both console and file output.
Replaces scattered print statements with structured logging.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    console: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance with console and optional file output.

    Args:
        name: Logger name (typically __name__ of calling module).
        log_file: Optional path to log file. If None, only console output.
        level: Logging level (default: logging.INFO).
        console: Whether to also output to console (default: True).

    Returns:
        Configured logger instance.

    Example:
        >>> logger = setup_logger(__name__, log_file="simulation.log")
        >>> logger.info("Starting visibility simulation...")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Format for all handlers
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an already-configured logger instance.

    Args:
        name: Logger name.

    Returns:
        Logger instance (or root logger if not yet configured).
    """
    return logging.getLogger(name)
