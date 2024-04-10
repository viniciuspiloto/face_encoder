import logging


class Logger:
    """Logger Class"""

    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(ch)

    def debug(self, message: str):
        """Debug

        Args:
            message (str): The message to be logged
        """
        self.logger.debug(message)

    def info(self, message):
        """Info

        Args:
            message (str): The message to be logged
        """
        self.logger.info(message)

    def warning(self, message):
        """Warning

        Args:
            message (str): The message to be logged
        """
        self.logger.warning(message)

    def error(self, message):
        """Error

        Args:
            message (str): The message to be logged
        """
        self.logger.error(message)

    def exception(self, message):
        """Exception

        Args:
            message (str): The message to be logged
        """
        self.logger.exception(message)
