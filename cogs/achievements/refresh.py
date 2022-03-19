from discord.ext import commands
from discord.ext.commands import has_any_role, MissingAnyRole

from data import config


class Achivements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_any_role(config.ID_OWNER, config.ID_ROLE_ADMIN, config.ID_ROLE_MODERATOR)
    async def refresh(self, ctx):
        pass

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            return await ctx.send('Sorry, you do not have permissions to do refresh!')


def setup(bot):
    bot.add_cog(Achivements(bot))
