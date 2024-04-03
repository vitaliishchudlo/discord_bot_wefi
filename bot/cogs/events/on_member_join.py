import random
from logging import getLogger

import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from nextcord.utils import get

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models import UserCaptchaModel
from discord_bot_wefi.bot.database.models import UserModel
from discord_bot_wefi.bot.misc.config import BotLoggerName
from discord_bot_wefi.bot.misc.config import ID_TEXT_CHANNEL_FOR_WELCOME, ID_ROLE_AFTER_VERIFICATION, ID_ROLE_BOT

logger = getLogger(BotLoggerName)


async def captcha_check(button: nextcord.ui.Button, interaction: nextcord.Interaction):
    user = session.query(UserModel).filter_by(
        discord_id=interaction.user.id).first()
    validated_code = session.query(
        UserCaptchaModel).filter_by(user_id=user.id).first()

    if not validated_code or not button.label == validated_code.code:

        new_captcha_solution = str(random.randint(1, 10))

        logger.info(
            f'[EVENT] User {user.username} is not verified. Old captcha code: {validated_code}. New captcha code: {new_captcha_solution}')

        user_captcha = session.query(UserCaptchaModel).filter_by(user_id=user.id).first()
        if not user_captcha:
            user_captcha = UserCaptchaModel(code=new_captcha_solution, verified=False, user_id=user.id)
            session.add(user_captcha)
        else:
            user_captcha.code = new_captcha_solution
        session.commit()

        return await interaction.response.edit_message(content=f'⛔ {interaction.user.mention} **NOT verified!**\n\n'
                                                               f'Please, select a number below: **{new_captcha_solution}**',
                                                       view=CaptchaAnswer())
    else:
        user_captcha = session.query(
            UserCaptchaModel).filter_by(user_id=user.id).first()
        user_captcha.verified = True
        session.commit()

        role_to_give = get(interaction.guild.roles, id=ID_ROLE_AFTER_VERIFICATION)
        await interaction.user.add_roles(role_to_give)
    logger.info(
        f'[EVENT] User {user.username} verified successfully with captcha code: {validated_code}')
    return await interaction.response.edit_message(content=f'✅ {interaction.user.mention} verified!', view=None)


class CaptchaAnswer(nextcord.ui.View):
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    random.shuffle(labels)

    button_styles = [ButtonStyle.blurple, ButtonStyle.green, ButtonStyle.secondary, ButtonStyle.danger]

    @nextcord.ui.button(label=labels[0], style=random.choice(button_styles))
    async def answer_1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[1], style=random.choice(button_styles))
    async def answer_2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[2], style=random.choice(button_styles))
    async def answer_3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[3], style=random.choice(button_styles))
    async def answer_4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[4], style=random.choice(button_styles))
    async def answer_5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[5], style=random.choice(button_styles))
    async def answer_6(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[6], style=random.choice(button_styles))
    async def answer_7(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[7], style=random.choice(button_styles))
    async def answer_8(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[8], style=random.choice(button_styles))
    async def answer_9(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)

    @nextcord.ui.button(label=labels[9], style=random.choice(button_styles))
    async def answer_10(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        return await captcha_check(button, interaction)


class OnMemberJoin(Cog):
    def __init__(self, bot: Bot):
        self.welcome_chat = None
        self.bot = bot

    def save_user_to_db(self, member):
        user = UserModel(discord_id=member.id, username=member.name)
        session.add(user)
        session.commit()
        return user

    @commands.Cog.listener()
    async def on_member_join(self, member):

        await self.bot.wait_until_ready()

        if member.bot:
            if not ID_ROLE_BOT:
                logger.warning('[EVENT] Parameter "ID_ROLE_BOT" is not filled in misc/config.py file')
                return
            role = get(member.guild.roles, id=ID_ROLE_BOT)
            await member.add_roles(role)
            logger.info(f'[EVENT] Bot {member.name} joined the server. Role {role.name} was added to the bot')
            return

        if not ID_TEXT_CHANNEL_FOR_WELCOME:
            logger.warning('[EVENT] Parameter "ID_TEXT_CHANNEL_FOR_WELCOME" is not filled in misc/config.py file')
            return

        self.welcome_chat = self.bot.get_channel(ID_TEXT_CHANNEL_FOR_WELCOME)

        captcha_solution = str(random.randint(1, 10))

        user = session.query(UserModel).filter_by(discord_id=member.id).first()
        if not user:
            user = self.save_user_to_db(member)

        user_captcha = session.query(
            UserCaptchaModel).filter_by(user_id=user.id).first()
        if not user_captcha:
            user_captcha = UserCaptchaModel(
                code=captcha_solution, verified=False, user_id=user.id)
            session.add(user_captcha)
        else:
            user_captcha.code = captcha_solution
        session.commit()

        logger.info(
            f'[EVENT] User {member.name} joined the server; User data: Discord id - {member.id} | ID in the DB - {user.id} | Captcha - {user_captcha.code}')
        await self.welcome_chat.send(
            f'Hey, {member.mention}, welcome to the {self.bot.guilds[0].name} 👋 \n'
            'You need to be **verified**.\n\n'
            f'Please, select a number: **{captcha_solution}**', view=CaptchaAnswer())


def register_cog(bot: Bot) -> None:
    bot.add_cog(OnMemberJoin(bot))
