import logging

from nextcord.ext.commands import Bot

from .user_activity import UserActivityTask
from .faceit_tracker import FaceitLvlTracker


def start_all_loops(bot: Bot) -> None:
    UserActivityTask(bot).activity_voice_channels_check.start()
    FaceitLvlTracker(bot).faceit_lvl_check.start()

    logging.info('[TASK] Tasks (loops) functions starting... OK')
