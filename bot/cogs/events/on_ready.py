from logging import getLogger

import nextcord
from nextcord import Game, Streaming, Activity, CustomActivity
from nextcord.ext import commands
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Cog

from discord_bot_wefi.bot.database import session, UserModel
from discord_bot_wefi.bot.misc.config import BotLoggerName
from discord_bot_wefi.bot.tasks.runner import start_all_loops
from discord_bot_wefi.bot.misc.config import BotStatusText

logger = getLogger(BotLoggerName)


class OnReady(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def init_users_with_db(self):
        all_members_on_server = [member for member in self.bot.get_all_members()]
        all_members_on_database = session.query(UserModel).all()
        all_members_discord_ids_on_database = [x.discord_id for x in all_members_on_database]

        for member in all_members_on_server:
            member_model = UserModel(
                discord_id=member.id,
                username=member.name
            )
            if member_model.discord_id in all_members_discord_ids_on_database:
                continue
            session.add(member_model)
            session.commit()

        logger.info(f'Initialization users... OK')
        return

    @commands.Cog.listener()
    async def on_ready(self):
        self.init_users_with_db()  # If bot was turn off - add all the new users to the database
        start_all_loops(self.bot)
        logger.info('The Bot has been successfully launched :-)\n')
        await self.bot.change_presence(activity=Activity(type=nextcord.ActivityType.listening, name=BotStatusText))


def register_cog(bot: Bot) -> None:
    bot.add_cog(OnReady(bot))
