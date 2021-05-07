import logging

from datetime import date
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from os.path import abspath, dirname


class SpeakerVerificationLogger(Logger):
    def __init__(
            self,
            name: str,
            log_file: str = "",
            log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            *args,
            **kwargs
    ):
        if log_file == "":
            file_path = dirname(abspath(__file__))
            today = date.today()
            self.log_file = f'{file_path}/../logs/{today.strftime("%d-%m-%Y")}.log'
        else:
            self.log_file = log_file

        self.formatter = logging.Formatter(log_format)

        Logger.__init__(self, name, *args, **kwargs)

        self.addHandler(self.get_console_handler())
        if self.log_file:
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
