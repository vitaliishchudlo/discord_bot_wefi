from discord.ext import commands
from bot import bot


class CogsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, name: str):
        try:
            bot.reload_extension(f'cogs.{name}')
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog reloaded')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, name: str):
        try:
            bot.unload_extension(f'cogs.{name}')
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog unloaded')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, name: str):
        try:
            bot.load_extension(f'cogs.{name}')
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog loaded')


def setup(bot):
    bot.add_cog(CogsManager(bot))
