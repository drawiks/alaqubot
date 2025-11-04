
class LogManager:
    
    _instance = None 
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_path: str, console_level: str = "TRACE"):
        if hasattr(self, "logger"):
            return
        
        from loguru import logger
        from pathlib import Path
        import sys
        
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