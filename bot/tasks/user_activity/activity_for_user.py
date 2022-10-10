from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot


class __UserActivity(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='my_activity')
    async def activity_voice_channels_check(self, ctx):
        await self.bot.wait_until_ready()


def register_cog(bot: Bot) -> None:
    bot.add_cog(__UserActivity(bot))
