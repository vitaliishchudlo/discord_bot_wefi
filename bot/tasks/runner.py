import logging

from nextcord.ext.commands import Bot

from .user_activity import UserActivityTask
from .faceit_tracker import FaceitLvlTracker


def start_all_loops(bot: Bot) -> None:
    user_activity_task = UserActivityTask(bot)
    faceit_tracker_task = FaceitLvlTracker(bot)

    if not user_activity_task.activity_voice_channels_check.is_running():
        print(111, bool(user_activity_task.activity_voice_channels_check.is_running()))
        user_activity_task.activity_voice_channels_check.start()

    if not faceit_tracker_task.faceit_lvl_check.is_running():
        print(222, bool(faceit_tracker_task.faceit_lvl_check.is_running()))
        faceit_tracker_task.faceit_lvl_check.start()

    logging.info('[TASK] Tasks (loops) functions starting... OK')
