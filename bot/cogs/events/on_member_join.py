import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from nextcord.utils import get

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models import UserCaptchaModel
from discord_bot_wefi.bot.database.models import UserModel
from discord_bot_wefi.bot.misc.config import ID_TEXT_CHANNEL_FOR_WELCOME, BOT_PREFIX, ID_ROLE_AFTER_VERIFICATION
from discord_bot_wefi.bot.misc.util import Captcha


class OnMemberJoin(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def save_user_to_db(self, member):
        user = UserModel(discord_id=member.id, username=member.name, discriminator=member.discriminator)
        session.add(user)
        session.commit()
        return user

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()

        if ID_TEXT_CHANNEL_FOR_WELCOME:
            self.welcome_chat = self.bot.get_channel(
                ID_TEXT_CHANNEL_FOR_WELCOME)

        captcha = Captcha(member_id=member.id)
        captcha.save_picture()

        user = session.query(UserModel).filter_by(discord_id=member.id).first()
        if not user:
            user = self.save_user_to_db(member)

        user_captcha = session.query(
            UserCaptchaModel).filter_by(user_id=user.id).first()
        if not user_captcha:
            user_captcha = UserCaptchaModel(
                code=captcha.get_code(), verified=False, user_id=user.id)
            session.add(user_captcha)
        else:
            user_captcha.code = captcha.get_code()
        session.commit()

        await self.welcome_chat.send(
            f'Hey, {member.mention}, welcome to the {self.bot.guilds[0].name} 👋 \n'
            'To get more access, you need to be **verified**.\n\n'
            f'Please, enter the command:  **{BOT_PREFIX}reg** __code from image__',
            file=captcha.get_file())


class MemberVerification(commands.Cog):
    def __init__(self, bot):
        self.code = None
        self.bot = bot

    @nextcord.slash_command(name='reg', description='Registration. Input code')
    async def reg(self, ctx, code: str):
        await self.bot.wait_until_ready()

        if not code:
            return await ctx.response.send_message('Please, enter verification code!')

        self.code = code.lower().replace(' ', '')

        user = session.query(UserModel).filter_by(
            discord_id=ctx.user.id).first()
        validated_code = session.query(
            UserCaptchaModel).filter_by(user_id=user.id).first()

        if not validated_code or not self.code == validated_code.code.lower():
            captcha = Captcha(member_id=ctx.user.id)
            captcha.save_picture()

            self.user_captcha = session.query(
                UserCaptchaModel).filter_by(user_id=user.id).first()
            if not self.user_captcha:
                user_captcha = UserCaptchaModel(
                    code=captcha.get_code(), verified=False, user_id=user.id)
                session.add(user_captcha)
            else:
                self.user_captcha.code = captcha.get_code()
            session.commit()

            return await ctx.response.send_message(
                f'⛔ {ctx.user.mention} **NOT verified!**\n\n'
                f'Please, enter the command:  **{BOT_PREFIX}reg** __code from image__', file=captcha.get_file())
        else:
            self.user_captcha = session.query(
                UserCaptchaModel).filter_by(user_id=user.id).first()
            self.user_captcha.verified = True
            session.commit()

            role_to_give = get(ctx.guild.roles, id=ID_ROLE_AFTER_VERIFICATION)
            await ctx.user.add_roles(role_to_give)

        return await ctx.send(f'✅ {ctx.user.mention} verified!')


def register_cog(bot: Bot) -> None:
    bot.add_cog(OnMemberJoin(bot))
    bot.add_cog(MemberVerification(bot))
