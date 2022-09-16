import discord
from discord.ext import commands

from data import config
from manage_extensions import manage_extensions

if not config.BOT_TOKEN:
    print('[ERROR]: Fill the BOT_TOKEN variable in the .env file (example in .env.tmp).')
    exit(-1)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)

manage_extensions(bot)

bot.run(config.BOT_TOKEN)
