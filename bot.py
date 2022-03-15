import discord
from discord.ext import commands

from data import config
import os
os.system('clear')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=('.', ';'), intents=intents)

bot.load_extension("cogs.events.on_ready")
bot.load_extension("cogs.events.on_member_join")

bot.load_extension("cogs.cogs_manager")

bot.load_extension("cogs.achivements.achivements")
bot.load_extension("cogs.system.clear_chat")
bot.load_extension("cogs.system.json")

bot.run(config.BOT_TOKEN)
