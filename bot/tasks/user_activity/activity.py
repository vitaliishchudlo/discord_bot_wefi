from datetime import datetime

from nextcord.ext import commands, tasks
from nextcord.ext.commands import Cog, Bot

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import User
from discord_bot_wefi.bot.database.models.users_activity import UserActivity
from discord_bot_wefi.bot.misc.config import ROLE_ID_FOR_ACTIVITY_TRACK


class __UserActivity(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.role_id_for_activity_track = ROLE_ID_FOR_ACTIVITY_TRACK

        self.guild_data = self.bot.guilds[0]
        self.afk_channel = self.guild_data.afk_channel
        self.voice_channels = self.guild_data.voice_channels

    def get_members_in_voice_channels(self):
        online_members_in_voice_chats = []

        for channel in self.voice_channels:
            members = channel.members

            # Filter AFK channel (if exists)
            if channel == self.afk_channel:
                continue
            # Filter if no one is in the voice channel
            if not members:
                continue

            # Filter bots (if exists)
            for member in members:
                if member.bot:
                    members.remove(member)

            # Filter minimum member in one voice channel
            if len(members) <= 1:
                continue

            # Filter role (if exists)
            for member in members:
                if self.role_id_for_activity_track:
                    if self.role_id_for_activity_track in member.roles:
                        online_members_in_voice_chats.append(member)
                else:
                    online_members_in_voice_chats.append(member)

        return online_members_in_voice_chats

    @tasks.loop(seconds=10)
    @commands.Cog.listener()
    async def activity_check(self, *args, first_time=False):
        await self.bot.wait_until_ready()

        if self.role_id_for_activity_track:
            self.role_id_for_activity_track = self.bot.guilds[0].get_role(self.role_id_for_activity_track)

        online_members_in_voice_chats = self.get_members_in_voice_channels()

        import ipdb; ipdb.set_trace(context=5)


        for member in online_members_in_voice_chats:
            today_date = datetime.strptime(datetime.strftime(datetime.today(), "%d/%m/%Y"), "%d/%m/%Y")
            user = session.query(User).filter_by(discord_id=member.id).first()
            user_activity = session.query(UserActivity).filter_by(user_id=user.id, date=today_date).first()
            if user_activity:
                user_activity.active_minutes += 1
                session.commit()
                continue
            user_activity = UserActivity(date=today_date, active_minutes=1, user_id=user.id)
            session.add(user_activity)
            session.commit()
            

        print('Done. Sleeping 5 seconds')


def register_cog(bot: Bot) -> None:
    bot.add_cog(__UserActivity(bot))
