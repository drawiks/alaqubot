
from src.config import LOG_PATH

from dlogger import logger

logger.configure(
    log_file=LOG_PATH,
    rotation="20MB",
    retention="7 days",
    compression=True
)
