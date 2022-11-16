from abc import ABC
from datetime import date
from logging import getLogger, FileHandler, DEBUG, Formatter
from os import path, mkdir
from pathlib import Path

from discord_bot_wefi.bot.misc.config import BotLoggerName


class AbstractLogger(ABC):
    def __init__(self, logger_name, file_name, formatter, logger_lever=DEBUG, file_handler_level=DEBUG):
        self.logs_dir = f'{Path().absolute()}/logs'
        if not path.isdir(self.logs_dir):
            mkdir(self.logs_dir)

        self.logger = getLogger(name=logger_name)
        self.logger.propagate = False
        self.logger.setLevel(level=logger_lever)

        file_handler = FileHandler(filename=file_name)
        file_handler.setFormatter(fmt=formatter)
        file_handler.setLevel(file_handler_level)

        self.logger.addHandler(hdlr=file_handler)


class BotLogger(AbstractLogger):
    def __init__(self):
        self.filename = f'{Path().absolute()}/logs/BOT_logs_{date.today()}.log'
        self.logger_name = BotLoggerName
        self.formatter = Formatter(
            f'| %(asctime)s | %(filename)-21s | %(lineno)-3d | %(levelname)s: %(message)s'
        )
        super().__init__(file_name=self.filename, logger_name=self.logger_name, formatter=self.formatter)
