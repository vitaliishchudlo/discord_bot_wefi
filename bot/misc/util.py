import os
import random

from captcha.image import ImageCaptcha
from nextcord import File

from discord_bot_wefi.bot.misc.config import CAPTCHAS_SAVING_PATH, CAPTCHA_PREFIX


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
                raise TypeError(
                    'You need to specify "custom_file_name" argument or input it in the config file')
        image = ImageCaptcha(width=500, height=100)
        image.write(self._code, self.file_path)

        return File(self.file_path)


def calculatetime(fn):
    def wrapper(given_minutes):
        given_minutes = int(given_minutes)

        days = None
        hours = None
        minutes = None

        if given_minutes < 60:
            minutes = str(given_minutes)

        if given_minutes < 1440:
            hours = given_minutes // 60
            given_minutes -= hours * 60
            minutes = str(given_minutes)

        if given_minutes >= 1440:
            days = given_minutes // 60 // 24
            given_minutes -= days * 24 * 60
            if not given_minutes < 60:
                hours = given_minutes // 60
                given_minutes -= hours * 60
            else:
                hours = str(0)
            minutes = str(given_minutes)

        result_data = fn(days=days, hours=hours, minutes=minutes)
        return result_data

    return wrapper


@calculatetime
def minutes_converter(**kwargs):
    response = ''
    if kwargs.get('days'):
        response += f'{kwargs.get("days")} d. '
    if kwargs.get('hours'):
        response += f'{kwargs.get("hours")} h. '
    if kwargs.get('minutes'):
        response += f'{kwargs.get("minutes")} min. '
    return response
