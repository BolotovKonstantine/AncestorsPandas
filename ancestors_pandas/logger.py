"""
Logging configuration for AncestorsPandas.

This module provides a centralized logging configuration for the project.
"""

import logging
import os
import sys
from typing import Optional


def setup_logger(
    name: str = "ancestors_pandas",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
    file_mode: str = 'a'
) -> logging.Logger:
    """
    Set up and configure a logger.

    Parameters:
    -----------
    name : str, optional
        Name of the logger. Default is "ancestors_pandas".
    level : int, optional
        Logging level. Default is logging.INFO.
    log_file : str, optional
        Path to the log file. If None, file logging is disabled.
    console_output : bool, optional
        Whether to output logs to the console. Default is True.
    file_mode : str, optional
        File mode for the log file. Default is 'a' (append).

    Returns:
    --------
    logging.Logger
        Configured logger instance.

    Raises:
    -------
    TypeError
        If parameters have incorrect types.
    ValueError
        If level is not a valid logging level or file_mode is not valid.
    """
    # Validate input parameters
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")

    if not isinstance(level, int):
        raise TypeError(f"level must be an integer, got {type(level).__name__}")

    # Check if level is a valid logging level
    valid_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    if level not in valid_levels:
        raise ValueError(f"level must be a valid logging level: {valid_levels}")

    if log_file is not None and not isinstance(log_file, str):
        raise TypeError(f"log_file must be a string or None, got {type(log_file).__name__}")

    if not isinstance(console_output, bool):
        raise TypeError(f"console_output must be a boolean, got {type(console_output).__name__}")

    if not isinstance(file_mode, str):
        raise TypeError(f"file_mode must be a string, got {type(file_mode).__name__}")

    # Check if file_mode is valid
    valid_modes = ['a', 'w', 'x']
    if file_mode not in valid_modes:
        raise ValueError(f"file_mode must be one of {valid_modes}, got {file_mode}")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if log_file is provided
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file, mode=file_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create a default logger instance
logger = setup_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Parameters:
    -----------
    name : str, optional
        Name of the logger. If None, the default logger is returned.

    Returns:
    --------
    logging.Logger
        Logger instance.

    Raises:
    -------
    TypeError
        If name is not a string or None.
    """
    # Validate input
    if name is not None and not isinstance(name, str):
        raise TypeError(f"name must be a string or None, got {type(name).__name__}")

    if name:
        return logging.getLogger(f"ancestors_pandas.{name}")
    return logger
