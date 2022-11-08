from nextcord.ext.commands import Bot

# from discord_bot_wefi.bot.cogs import events as reg_events_cog
# from discord_bot_wefi.bot.cogs import user_activity as reg_user_activity
from discord_bot_wefi.bot import cogs as reg_cogs


def register_all_cogs(bot: Bot) -> None:
    """
    For the future:
        Implement the "register_all_cogs" method as a filter that
        will load only those cogs that are in the config.yaml file;

        data = read_config_yaml()['cogs']
    """
    cogs_for_register = (
        reg_cogs.events.register_cog,
        reg_cogs.activity.register_cog,

    )
    for cog in cogs_for_register:
        cog(bot)
