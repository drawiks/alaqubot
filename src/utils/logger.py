
from loguru import logger
from pathlib import Path
import sys

class LogManager:
    def __init__(self, log_path: str, console_level: str = "TRACE"):
        self._log_file = Path(log_path)
        self._log_file.parent.mkdir(parents=True, exist_ok=True)

        logger.remove()
        logger.add(sys.stdout, level=console_level)

        logger.add(
            self._log_file,
            level="TRACE",
            rotation="500 KB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
        )

        self.logger = logger