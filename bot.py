import os

import discord
from discord.ext import commands

from data import config

os.system('clear')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=(config.BOT_PREFIX, ';'), intents=intents)

bot.load_extension('cogs.events.on_ready')
bot.load_extension('cogs.events.on_member_join')

bot.load_extension('cogs.cogs_manager')

bot.load_extension('cogs.achievements.refresh')
bot.load_extension('cogs.achievements.achievements')
bot.load_extension('cogs.system.clear_chat')
bot.load_extension('cogs.system.json')

bot.run(config.BOT_TOKEN)
