from discord.ext import commands

from discord_bot_wefi.database.db import db_conn


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print('Starting Bot...')
        if db_conn:
            print('Database connection...OK')
        else:
            print('Database connection...ERROR')


def setup(bot):
    bot.add_cog(OnReady(bot))
