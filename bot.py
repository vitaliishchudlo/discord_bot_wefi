import discord
from discord.ext import commands

from data import config
import os
os.system('clear')

bot = commands.Bot(command_prefix=('.', ';'), intents=discord.Intents.all())

bot.load_extension("cogs.events.on_ready")

bot.load_extension("cogs.cogs_manager")

bot.load_extension("cogs.achivements.achivements")
bot.load_extension("cogs.system.clear_chat")
bot.load_extension("cogs.system.json")

bot.run(config.BOT_TOKEN)
