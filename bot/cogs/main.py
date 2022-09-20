from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.cogs.admin import register_admin_cogs
from discord_bot_wefi.bot.cogs.other import register_other_cogs
from discord_bot_wefi.bot.cogs.user import register_user_cogs


def register_all_cogs(bot: Bot) -> None:
    cogs = (
        register_user_cogs,
        register_admin_cogs,
        register_other_cogs,
    )
    for cog in cogs:
        cog(bot)
