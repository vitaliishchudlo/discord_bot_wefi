from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs import admin as reg_admin_cogs

def register_all_cogs(bot: Bot) -> None:
    """
    For the future:
        Implement the "register_all_cogs" method as a filter that
        will load only those cogs that are in the config.yaml file;

        data = read_config_yaml()['cogs']
    """
    cogs = (
        reg_admin_cogs.main.register_admin_cogs,
        reg_admin_cogs.second.register_admin_cogs,

    )
    for cog in cogs:
        cog(bot)

