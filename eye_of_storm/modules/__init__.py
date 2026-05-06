"""Eye of the Storm — Base module."""

from abc import ABC, abstractmethod
from utils.logger import setup_logger


class BaseModule(ABC):
    """Base class for all EOTS modules."""

    def __init__(self, target: str, config, verbose: bool = False):
        self.target  = target
        self.config  = config
        self.verbose = verbose
        self.logger  = setup_logger(self.__class__.__name__)

    @abstractmethod
    def run(self) -> dict:
        """Execute the module and return a results dict."""

    def log(self, msg: str):
        if self.verbose:
            self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warn(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)
