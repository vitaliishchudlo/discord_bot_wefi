import shutil

from nextcord import Game
from nextcord.ext import commands
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Cog

from discord_bot_wefi.bot.database import session, UserModel
from discord_bot_wefi.bot.misc.util import BColors
from discord_bot_wefi.bot.tasks.runner import start_all_loops


class OnMemberJoin(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass





def register_cog(bot: Bot) -> None:
    bot.add_cog(OnMemberJoin(bot))
