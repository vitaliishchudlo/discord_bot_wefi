import discord
from discord.ext import commands

from data import config

bot = commands.Bot(command_prefix=('.', ';'), intents=discord.Intents.all())


@bot.command()
@commands.is_owner()
async def reload(ctx, *, name: str):
    try:
        bot.reload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send(f'"**{name}**" Cog reloaded')


@bot.command()
@commands.is_owner()
async def unload(ctx, *, name: str):
    try:
        bot.unload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send(f'"**{name}**" Cog unloaded')


@bot.command()
@commands.is_owner()
async def load(ctx, *, name: str):
    try:
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send(f'"**{name}**" Cog loaded')


bot.load_extension("cogs.achivements.achivements")
bot.load_extension("cogs.events.on_ready")
bot.load_extension("cogs.system.clear_chat")

bot.run(config.BOT_TOKEN)
