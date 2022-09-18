import os

import discord_bot_wefi.bot.config as config
from nextcord import Intents, Activity, ActivityType
from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs import register_all_cogs
from discord_bot_wefi.bot.database.db_init import create_db

from discord_bot_wefi.test_file import go_test

def start_bot():
    # Checking whether the user has added a bot token
    if not config.BOT_TOKEN:
        print('[ERROR]: Fill the BOT_TOKEN variable in the .env file (example in .env.tmp).')
        exit(-1)

    if not os.path.isfile('database.sqlite'):
        create_db()
    go_test()



    # Set custom status to "Listening to ?help"
    # ActivityType: unknown=-1, playing=0, streaming=1, listening=2, watching=3, custom=4, competing=5, unknown=-1

    # activity = Activity(
    #     type=ActivityType.listening, name=f"{config.BOT_PREFIX}help"
    # )

    # Allows privledged intents for monitoring members joining, roles editing, and role assignments
    # These need to be enabled in the developer portal as well
    # intents = Intents.default()

    # Required in order to read messages (eg. prefix commands)
    # intents.message_content = True

    # To enable the guilds priveleged intent:
    # intents.guilds = True

    # To enable the members priveleged intent:
    # intents.members = True

    # To enable the presence related events:
    # intents.presences = False

    # bot = Bot(command_prefix=config.CMD_PREFIX, intents=intents)

    # register_all_cogs(bot)
    # register_models()
    # manage_extensions(bot) # my

    # bot.run(Env.TOKEN)
    # bot.run(config.BOT_TOKEN) # my
