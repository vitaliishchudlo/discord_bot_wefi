import os
import shutil
from datetime import datetime
from pathlib import Path

from nextcord import Embed, File, Color
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Cog, Bot

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import UserModel
from discord_bot_wefi.bot.database.models.users_activity import UserActivityModel
from discord_bot_wefi.bot.misc.config import ID_ROLE_FOR_ACTIVITY_TRACK, \
    ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY


class UserActivityTask(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.role_id_for_activity_track = ID_ROLE_FOR_ACTIVITY_TRACK

        self.date_for_report = datetime.strptime(datetime.strftime(
            datetime.today(), '%d/%m/%Y'), '%d/%m/%Y')

        self.report_color = None
        self.times_runner = 0

    async def get_members_in_voice_channels(self):
        self.guild_data = self.bot.guilds[0]
        self.afk_channel = self.guild_data.afk_channel
        self.voice_channels = self.guild_data.voice_channels

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

    async def get_today_db_file_for_report(self):
        DB_CORE_DIR = f'{Path().absolute()}/bot/database'
        DB_ARCHIVE_DIR = f'{DB_CORE_DIR}/archive'
        if not os.path.isdir(DB_ARCHIVE_DIR):
            os.mkdir(DB_ARCHIVE_DIR)

        """
        -Change next to the PATH_DATABASE from conf.yaml;
        - Find in project where it can meet too;
        - Fix it like: 'DB_NAME' only;
        """

        if os.path.isfile(f'{DB_CORE_DIR}/database.sqlite'):
            today_formatted_date = datetime.strftime(datetime.today(), '%d_%m_%Y')
            src_file = f'{DB_CORE_DIR}/database.sqlite'
            dst_file = f'{DB_ARCHIVE_DIR}/db_{today_formatted_date}.sqlite'
            shutil.copy2(src_file, dst_file)
            return File(dst_file)

    @tasks.loop(seconds=60)
    @commands.Cog.listener()
    async def activity_voice_channels_check(self, *args):
        await self.bot.wait_until_ready()

        today_date = datetime.strptime(datetime.strftime(
            datetime.today(), '%d/%m/%Y'), '%d/%m/%Y')

        # Every day activity report
        if not self.date_for_report == today_date:
            if ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY:
                self.channel_report = self.bot.get_channel(
                    ID_TEXT_CHANNEL_FOR_REPORT_ACTIVITY)

                users_names = []
                users_activity = []
                active_users_for_today = session.query(UserActivityModel).filter_by(
                    date=self.date_for_report).order_by(UserActivityModel.minutes_in_voice_channels.desc()).all()

                if active_users_for_today:
                    for user in active_users_for_today:
                        users_names.append(user.user.username)
                        users_activity.append(
                            str(user.minutes_in_voice_channels))
                else:
                    users_names.append(
                        '__No one has visited the server today__')
                    users_activity.append(':pleading_face:')

                if self.report_color == Color.teal().blue():
                    self.report_color = Color.teal().yellow()
                else:
                    self.report_color = Color.teal().blue()

                embed = Embed(
                    title=f"Activity report for {datetime.strftime(self.date_for_report, '%d/%m/%Y')}",
                    description='This report shows activity in voice channels.', color=self.report_color)
                embed.add_field(name='User', value='\n'.join(
                    users_names), inline=True)
                embed.add_field(name='Minutes', value='\n'.join(
                    users_activity), inline=True)

                self.db_file_for_report = await self.get_today_db_file_for_report()

                await self.channel_report.send(embed=embed, file=self.db_file_for_report)
                self.date_for_report = today_date
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        if self.role_id_for_activity_track:
            self.role_id_for_activity_track = self.bot.guilds[0].get_role(
                self.role_id_for_activity_track)

        online_members_in_voice_chats = await self.get_members_in_voice_channels()

        for member in online_members_in_voice_chats:
            user = session.query(UserModel).filter_by(
                discord_id=member.id).first()
            user_activity = session.query(UserActivityModel).filter_by(
                user_id=user.id, date=today_date).first()
            if user_activity:
                user_activity.minutes_in_voice_channels += 1
                session.commit()
                continue
            user_activity = UserActivityModel(
                date=today_date, minutes_in_voice_channels=1, user_id=user.id)
            session.add(user_activity)
            session.commit()


def register_cog(bot: Bot) -> None:
    bot.add_cog(UserActivityTask(bot))
