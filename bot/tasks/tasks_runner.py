from nextcord.ext.commands import Bot

from .user_activity import __UserActivity


def start_all_loops(bot: Bot) -> None:
    print('STARTING ALL LOOPS FUNCTION')
    __UserActivity(bot).activity_voice_channels_check.start(first_time=True)
