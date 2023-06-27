from logging import getLogger

from nextcord.ext.commands import Bot

from discord_bot_wefi.bot import cogs as reg_cogs
from discord_bot_wefi.bot.misc.config import BotLoggerName

logger = getLogger(BotLoggerName)


def register_all_cogs(bot: Bot) -> None:
    """
    For the future:
        Implement the "register_all_cogs" method as a filter that
        will load only those cogs that are in the config.yaml file;

        data = read_config_yaml()['cogs']
    """
    cogs_for_register = (
        reg_cogs.events.on_member_join.register_cog,
        reg_cogs.events.on_ready.register_cog,

        reg_cogs.activity.activity_for_user.register_cog,

        reg_cogs.json.json_info.register_cog,
        reg_cogs.logs_results.register_cog,

        reg_cogs.db_upload.register_cog,
    )
    # todo: можна імплементувати в init імпорт "as" from .db_upload import register_cog as db_upload_test
    # і тоді тут тільки: reg_cogs.db_upload_test
    for cog in cogs_for_register:
        cog(bot)

    logger.info('Cogs - registered successfully')