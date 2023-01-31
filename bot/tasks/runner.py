from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.misc.util import BColors
from .user_activity import UserActivityTask


def start_all_loops(bot: Bot) -> None:
    UserActivityTask(bot).activity_voice_channels_check.start()
    print(
        f'{BColors.SYSTEM}LOOPS(TASKS) FUNCTIONS: {BColors.OKGREEN}{BColors.BOLD}STARTED{BColors.ENDC}!')
