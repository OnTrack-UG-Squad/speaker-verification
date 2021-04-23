import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


class SpeakerVerificationLogger(Logger):
    def __init__(
            self,
            name: str = __file__,
            log_file: str = 'speaker_verification/logs/default.log',
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

    def get_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when="midnight")
        file_handler.setFormatter(self.formatter)
        return file_handler
