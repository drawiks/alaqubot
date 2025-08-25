
from loguru import logger
from pathlib import Path
import sys

class LogManager:
    def __init__(self, log_path: str, level: str = "INFO"):
        self._log_file = Path(log_path)
        self._level = level

        self._log_file.parent.mkdir(parents=True, exist_ok=True)

        logger.remove()
        logger.add(sys.stdout, level=self._level)
        logger.add(
            self._log_file,
            level=self._level,
            rotation="500 KB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
        )
        self.logger = logger