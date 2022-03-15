import os
import random

from captcha.image import ImageCaptcha
from discord import File
from discord.ext import commands

from data import config
from database.db import Database


def generate_captcha_text():
    global captcha_body
    way_to_generate = random.randint(1, 2)
    captcha_prefix = config.CAPTCHA_PREFIX
    if way_to_generate == 1:
        captcha_body = str(random.randint(1000, 9999))
    if way_to_generate == 2:
        captcha_body = str(random.choice(config.CAPTCHA_BODY))
    captcha_text = captcha_prefix + captcha_body
    return captcha_text


class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.bot.get_channel(config.ID_CHAT_WELCOME)
        if not welcome_channel:
            return print('Welcome channel not entered!')
        if not os.path.isdir('captchas'):
            os.mkdir('captchas')
        image = ImageCaptcha(width=500, height=100)
        captcha_text = generate_captcha_text()
        file_name = f'captchas/{member.id}.png'
        image.write(captcha_text, file_name)
        picture = File(open(file_name, 'rb'))
        Database().register_user(
            discord_id=member.id,
            user_name=member.name,
            captcha_text=captcha_text.lower()
        )
        await welcome_channel.send(
            f'👋 Hello, {member.mention}. Welcome to the We-Fi server!\n'
            f'You need to register. '
            f'Please, enter:  **{config.BOT_PREFIX}register** __captcha__',
            file=picture)


def setup(bot):
    bot.add_cog(Member(bot))
