from logging import getLogger, DEBUG, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from os import path, mkdir
from pathlib import Path

from discord_bot_wefi.bot.misc.config import BotLoggerName


class BotLogger:

    def __init__(self):
        self.logs_dir = f'{Path().absolute()}/logs'
        if not path.isdir(self.logs_dir):
            mkdir(self.logs_dir)

        self.bot_logs_file_name = 'bot_logs'

        self.filename = f'{self.logs_dir}/{self.bot_logs_file_name}.log'

        self.logger_name = BotLoggerName
        self.logger_level = DEBUG
        self.file_handler_level = DEBUG

        self.logger = getLogger(name=self.logger_name)
        self.logger.propagate = False
        self.logger.setLevel(level=self.logger_level)

        self.formatter = Formatter('| %(asctime)s | %(filename)-21s | %(lineno)-3d | %(levelname)s: %(message)s')

        self.fileTimeHandler = TimedRotatingFileHandler(self.filename, when='midnight', interval=1)
        self.fileTimeHandler.setFormatter(self.formatter)
        self.fileTimeHandler.setLevel(self.file_handler_level)
        self.fileTimeHandler.suffix = '%Y-%m-%d'
        self.fileTimeHandler.namer = lambda name: name.replace(".log", "") + ".log"

        self.consoleHandler = StreamHandler()
        self.consoleHandler.setFormatter(self.formatter)

        self.logger.addHandler(self.fileTimeHandler)
        self.logger.addHandler(self.consoleHandler)
