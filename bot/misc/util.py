from discord_bot_wefi.bot.misc.config import ID_TEXT_CHANNEL_FOR_WELCOME, CAPTCHAS_SAVING_PATH, CAPTCHA_PREFIX
import random

import os
import os
import random

from captcha.image import ImageCaptcha
from nextcord import File
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import commands

from discord_bot_wefi.bot.misc.config import ID_TEXT_CHANNEL_FOR_WELCOME, CAPTCHAS_SAVING_PATH, CAPTCHA_PREFIX


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Captcha:
    def __init__(self, member_id=None):
        self._init_path()
        self._code = self._generate_code()

        self.file_name = None
        self.file_path = None
        if member_id:
            self.file_name = str(member_id)
            self.file_path = CAPTCHAS_SAVING_PATH + '/' + self.file_name + '.png'

    def __repr__(self):
        return f'<{self.__class__.__name__}(captcha_text={self._code}, captcha_file_name={self.file_name})>'

    def get_code(self):
        return self._code

    def get_file(self):
        if os.path.isfile(self.file_path):
            return File(self.file_path)
        raise FileExistsError('Create file with method save_picture')

    def _init_path(self):
        if not os.path.isdir(CAPTCHAS_SAVING_PATH):
            os.mkdir(CAPTCHAS_SAVING_PATH)

    def _generate_code(self):
        captcha_integers = str(random.randint(1000, 9999))
        captcha_text = CAPTCHA_PREFIX + captcha_integers
        return captcha_text

    def save_picture(self, custom_file_name=None):
        if not self.file_name:
            if not custom_file_name:
                raise TypeError(f'You need to specify "custom_file_name" argument or input it in the config file')
        image = ImageCaptcha(width=500, height=100)
        image.write(self._code, self.file_path)

        return File(self.file_path)
