from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs import events as reg_events_cog
from discord_bot_wefi.bot.tasks import user_activity as reg_user_activity


def register_all_cogs(bot: Bot) -> None:
    """
    For the future:
        Implement the "register_all_cogs" method as a filter that
        will load only those cogs that are in the config.yaml file;

        data = read_config_yaml()['cogs']
    """
    cogs = (
        reg_events_cog.on_ready.register_cog,
        reg_user_activity.activity_for_user.register_cog,


    )
    for cog in cogs:
        cog(bot)
