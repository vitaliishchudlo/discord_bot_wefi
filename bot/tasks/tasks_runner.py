from nextcord.ext.commands import Bot

from .user_activity import __UserActivityTask


def start_all_loops(bot: Bot) -> None:
    print('STARTING ALL LOOPS FUNCTION')
    __UserActivityTask(bot).activity_voice_channels_check.start()
