from discord.ext import commands


class Achivements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def achi_add(self, ctx, user=None, game=None, type=None, count=1):
        if not user:
            return await ctx.reply('Enter the user')
        if not game:
            return await ctx.reply('Enter the game')
        if not type:
            return await ctx.reply('Enter the game type')

        return await ctx.reply(f'User: {user} Game: {game} Type: {type} Count: {count}')


def setup(bot):
    bot.add_cog(Achivements(bot))
