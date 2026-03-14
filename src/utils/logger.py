from src.config import LOG_PATH

from dlogger import logger

logger.configure(
    level="INFO",
    log_file=LOG_PATH,
    show_path=True,
    rotation="10MB",
    retention="7 days",
    compression=True,
    time_format="%d-%m %H:%M:%S",
)
