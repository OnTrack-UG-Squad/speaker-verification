import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


class SpeakerVerificationLogger(Logger):
    def __init__(
            self,
            log_file: str,
            name: str = __file__,
            log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            *args,
            **kwargs
    ):
        self.formatter = logging.Formatter(log_format)
        self.log_file = log_file

        Logger.__init__(self, name, *args, **kwargs)

        self.addHandler(self.get_console_handler())
        if log_file:
            self.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the| error up to parent
        self.propagate = False

    def get_console_handler(self) -> logging.StreamHandler:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self) -> logging.handlers.TimedRotatingFileHandler:
        file_handler = TimedRotatingFileHandler(self.log_file, when="midnight")
        file_handler.setFormatter(self.formatter)
        return file_handler
