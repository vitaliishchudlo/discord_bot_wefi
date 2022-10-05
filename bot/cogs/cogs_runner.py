from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs import events as reg_events_cog


def register_all_cogs(bot: Bot) -> None:
    """
    For the future:
        Implement the "register_all_cogs" method as a filter that
        will load only those cogs that are in the config.yaml file;

        data = read_config_yaml()['cogs']
    """
    cogs = (
        reg_events_cog.on_ready.register_cog,

    )
    for cog in cogs:
        cog(bot)
