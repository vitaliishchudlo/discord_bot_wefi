from discord.ext import commands


class ClearChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(ClearChat(bot))
