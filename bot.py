import os

import discord
from discord.ext import commands

from data import config


def clear():
    os.system('clear')


def load_extensions(bot):
    # = = = = = = Cogs Manager = = = = = =
    bot.load_extension('cogs.cogs_manager')

    # = = = = = = = = Events = = = = = = = =
    bot.load_extension('cogs.events.on_ready')
    bot.load_extension('cogs.events.on_member_join')

    # = = = = = = = = Commands  = = = = = = = =

    # Achievements
    bot.load_extension('cogs.achievements.refresh')
    bot.load_extension('cogs.achievements.achievements')

    # System
    bot.load_extension('cogs.system.clear_chat')
    bot.load_extension('cogs.system.json')


if __name__ == '__main__':
    if not config.BOT_TOKEN:
        print('[ERROR]: Enter the BOT_TOKEN in the .env file (example .env.tmp)')
        exit(-1)
    clear()
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)
    load_extensions(bot)
    bot.run(config.BOT_TOKEN)
