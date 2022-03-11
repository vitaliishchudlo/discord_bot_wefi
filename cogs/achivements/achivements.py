from discord.ext import commands


class Achivements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def achi_add(self, ctx):
        print('Achivements added! ')
        pass


def setup(bot):
    bot.add_cog(Achivements(bot))
