import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str, level=logging.DEBUG):
    """Function to set up a logger with rotation and specified settings."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    handler.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# Set up the logger
app_logger = setup_logger("my_app", "app.log")

if __name__ == "__main__":
    app_logger.info("This is an info message")
    app_logger.warning("This is a warning message")
    app_logger.error("This is an error message")
    app_logger.critical("This is a critical message")
