from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from discord_bot_wefi.bot.database.models import User, UserActivity
from discord_bot_wefi.bot.database import session

from datetime import datetime

from nextcord import Color
from nextcord import Embed
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Cog, Bot

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import User
from discord_bot_wefi.bot.database.models.users_activity import UserActivity
from discord_bot_wefi.bot.misc.config import ID_ROLE_FOR_ACTIVITY_TRACK, \
    ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY


class __UserActivity(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.report_color = Color.teal().purple()

    @commands.command(name='activity')
    async def activity_voice_channels_check(self, ctx):
        await self.bot.wait_until_ready()

        user = session.query(User).filter_by(discord_id=ctx.author.id).first()
        if not user:
            return await ctx.reply('Can`t find you in the database. Sorry.')
        user_activity = session.query(UserActivity).filter_by(user_id=user.id).order_by(UserActivity.date.desc()).all()
        if not user_activity:
            return await ctx.reply('Can`t find your activity in the database :(')

        result = {}
        for activity in user_activity:
            result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)


        embed = Embed(
            title=f"Activity report about _{user.username}_",
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
        embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

        await ctx.reply(embed=embed)



def register_cog(bot: Bot) -> None:
    bot.add_cog(__UserActivity(bot))
