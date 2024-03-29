import os
import sys
import time
from logging import getLogger

from nextcord import Intents, Activity, ActivityType
from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs import register_all_cogs
from discord_bot_wefi.bot.database.db_init import create_db
from discord_bot_wefi.bot.misc import config as conf
from discord_bot_wefi.bot.misc import env
from .bot_logger import BotLogger

logger = getLogger(conf.BotLoggerName)


def start_bot():
    # Init logger for bot
    BotLogger()

    # Set the right timezone
    if conf.timezone:
        os.environ['TZ'] = conf.timezone
        time.tzset()

    logger.info(f'Time: {time.strftime("%X %x %Z")}')

    # Checking whether the user has added a bot token
    token = env.BOT_TOKEN
    if not token or token == 'None':
        logger.error('You need to fill BOT_TOKEN variable in the .env file (example in the .env.tmp file)')
        exit(-1)

    # DataBase initialization:
    if not os.path.isfile(conf.PATH_DATABASE) or 'migrate' in sys.argv or 'hardmigrate' in sys.argv:
        if 'hardmigrate' in sys.argv:
            try:
                os.remove(conf.PATH_DATABASE)
            except Exception:
                pass
        create_db()

    # Set custom status to "Listening to ?help"
    # ActivityType: unknown=-1, playing=0, streaming=1, listening=2, watching=3, custom=4, competing=5, unknown=-1
    activity = Activity(
        type=ActivityType.listening, name=f'{conf.BOT_PREFIX}help'
    )

    """
                Intents
    Allows privledged intents for monitoring members joining, roles editing, and role assignments.
    These need to be enabled in the developer portal as well;

    To allow all intents                        or default:
        intents = Intents.all()                     intents = Intents.default()

    Required in order to read messages (eg. prefix commands):
        intents.message_content = True

    To enable the guilds priveleged intent:
        intents.guilds = True

    To enable the members priveleged intent:
        intents.members = True

    To enable the presence related events:
        intents.presences = False
    """

    intents = Intents.all()

    bot = Bot(command_prefix=conf.BOT_PREFIX, intents=intents)

    register_all_cogs(bot)

    bot.run(env.BOT_TOKEN)
