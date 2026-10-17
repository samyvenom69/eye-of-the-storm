"""Eye of the Storm — Logging setup."""

import logging
from rich.logging import RichHandler


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )
    return logging.getLogger(name)
