import os
import random

from captcha.image import ImageCaptcha
from discord import File
from discord.ext import commands
from discord.utils import get

from data import config
from database.db import Database


def generate_captcha(member_id, member_name):
    global captcha_body
    way_to_generate = random.randint(1, 2)
    captcha_prefix = config.CAPTCHA_PREFIX
    if way_to_generate == 1:
        captcha_body = str(random.randint(1000, 9999))
    if way_to_generate == 2:
        captcha_body = str(random.choice(config.CAPTCHA_BODY))
    captcha_text = captcha_prefix + captcha_body

    file_path = f'captchas/{member_id}.png'
    image = ImageCaptcha(width=500, height=100)
    image.write(captcha_text, file_path)
    Database().register_user(
        discord_id=member_id,
        user_name=member_name,
        captcha_text=captcha_text.lower()
    )
    return File(open(file_path, 'rb'))


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
        captcha_picture = generate_captcha(member.id, member.name)
        await welcome_channel.send(
            f'👋 Hello, {member.mention}. Welcome to the We-Fi server!\n'
            f'You need to register. '
            f'Please, enter:  **{config.BOT_PREFIX}register** __captcha__',
            file=captcha_picture)


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx, *, captcha: str):
        import ipdb; ipdb.set_trace(context=5)
        captcha_valid = Database().get_captcha_text(discord_id=ctx.author.id)
        if captcha_valid == captcha.lower():
            role_other = get(ctx.guild.roles, id=config.ID_ROLE_OTHER)
            await ctx.author.add_roles(role_other)
            return await ctx.send(
                f'✅ {ctx.author.mention} gets the role - {role_other}')
        captcha_picture = generate_captcha(ctx.author.id, ctx.author.name)
        await ctx.send(
            f'⛔ {ctx.author.mention} **Not validated!**\n'
            f'Here is a new captcha. '
            f'Please, enter:  **{config.BOT_PREFIX}register** __captcha__',
            file=captcha_picture)


def setup(bot):
    bot.add_cog(Member(bot))
    bot.add_cog(Register(bot))
