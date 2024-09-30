import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class AILog(logging.Logger):
    def __init__(self, name: str = "app", log_file: str = None, level=logging.DEBUG):
        super().__init__(name, level)

        if log_file is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
            log_file = f"./logs/{name}_{current_date}.log"

        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # Create a rotating file handler
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
        handler.setLevel(level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.addHandler(handler)

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)


if __name__ == "__main__":
    logger = AILog("my_logr")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
