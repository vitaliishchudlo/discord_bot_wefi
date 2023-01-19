import asyncio
from datetime import datetime

import nextcord
from nextcord import Color, ButtonStyle, Embed
from nextcord import SlashOption
from nextcord.ext.commands import Bot, Cog
from nextcord.member import Member
from nextcord.ui import Button, View
from sqlalchemy import func

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models import UserModel, UserActivityModel
from discord_bot_wefi.bot.misc.config import COGS_ACTIVITY_MESSAGE_EXPIRATION_TIME
from discord_bot_wefi.bot.misc.util import minutes_converter


DATE_COLUMN_NAME = 'ㅤㅤDate\ndd/mm/yyyy'
MEMBER_COLUMN_NAME = 'Member\nㅤ'
TIME_COLUMN_NAME = 'Time\nㅤ'


class UserActivity(Cog):
    def __init__(self, bot: Bot, msg_exp_time=60):
        self.bot = bot
        self.report_color = Color.teal().purple()

        if COGS_ACTIVITY_MESSAGE_EXPIRATION_TIME:
            self.msg_exp_time = COGS_ACTIVITY_MESSAGE_EXPIRATION_TIME
        else:
            self.msg_exp_time = msg_exp_time

    def format_time(self, time):
        return list(map(minutes_converter, time))

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def someone_activity_lasts_btn_callback(self, interaction):
        user = session.query(UserModel).filter_by(
            discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = session.query(UserActivityModel).filter_by(user_id=user.id).order_by(
            UserActivityModel.date.desc()).limit(25).all()

        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        for activity in user_activity:
            result[datetime.strftime(
                activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

        embed = Embed(
            title=f'Activity report about _{user.username}_',
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name=DATE_COLUMN_NAME,
                        value='\n'.join(result.keys()), inline=True)
        embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

        return await interaction.response.send_message(embed=embed)

    async def someone_activity_top_for_all_time_btn_callback(self, interaction):
        user = session.query(UserModel).filter_by(
            discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = session.query(UserActivityModel).filter_by(user_id=user.id). \
            order_by(UserActivityModel.minutes_in_voice_channels.desc()).limit(25).all()
        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        for activity in user_activity:
            result[datetime.strftime(
                activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

        embed = Embed(
            title=f'Activity report about _{user.username}_',
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name=DATE_COLUMN_NAME,
                        value='\n'.join(result.keys()), inline=True)
        embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

        return await interaction.response.send_message(embed=embed)

    async def someone_activity_summary_btn_callback(self, interaction):
        user = session.query(UserModel).filter_by(
            discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = \
            session.query(func.sum(UserActivityModel.minutes_in_voice_channels)).filter_by(
                user_id=user.id)[0][0]
        user_activity_period_start = session.query(
            UserActivityModel).filter_by(user_id=user.id).first()
        user_activity_period_end = session.query(UserActivityModel).filter_by(user_id=user.id).order_by(
            UserActivityModel.date.desc()).first()

        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        result[f'{datetime.strftime(user_activity_period_start.date, "%d/%m/%Y")} - '
               f'{datetime.strftime(user_activity_period_end.date, "%d/%m/%Y")}'] = str(user_activity)

        embed = Embed(
            title=f'Activity report about _{user.username}_',
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name=DATE_COLUMN_NAME,
                        value='\n'.join(result.keys()), inline=True)
        embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

        return await interaction.response.send_message(embed=embed)

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def everyones_activity_callback(self, interaction):
        async def everyone_activity_today_btn_callback(interaction):
            today_date = datetime.strptime(datetime.strftime(
                datetime.today(), '%d/%m/%Y'), '%d/%m/%Y')
            user_activity = session.query(UserActivityModel).filter_by(date=today_date).order_by(
                UserActivityModel.minutes_in_voice_channels.desc()).limit(25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find activity in the database :(')

            results_usernames = []
            results_minutes_in_voice_channels = []
            for activity in user_activity:
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(
                    str(activity.minutes_in_voice_channels))

            embed = Embed(
                title=f"Activity report for _{datetime.strftime(today_date, '%d/%m/%Y')}_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name=MEMBER_COLUMN_NAME, value='\n'.join(
                results_usernames), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(results_minutes_in_voice_channels)),
                            inline=True)

            return await interaction.response.send_message(embed=embed)

        async def everyone_activity_top_for_all_time_btn_callback(interaction):
            user_activity = session.query(UserActivityModel).order_by(
                UserActivityModel.minutes_in_voice_channels.desc()).limit(25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for activity in user_activity:
                results_date.append(datetime.strftime(
                    activity.date, '%d/%m/%Y'))
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(
                    str(activity.minutes_in_voice_channels))

            embed = Embed(
                title='Activity report for all-time',
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(results_date), inline=True)
            embed.add_field(name=MEMBER_COLUMN_NAME, value='\n'.join(
                results_usernames), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(results_minutes_in_voice_channels)),
                            inline=True)

            return await interaction.response.send_message(embed=embed)

        async def everyone_activity_summary_btn_callback(interaction):
            users_activity = session.query(UserActivityModel,
                                           func.sum(UserActivityModel.minutes_in_voice_channels),
                                           func.min(UserActivityModel.date),
                                           func.max(UserActivityModel.date)
                                           ).group_by(UserActivityModel.user_id).order_by(
                func.sum(UserActivityModel.minutes_in_voice_channels).desc()).all()

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for user_obj, user_activity_time, period_start, period_end in users_activity:
                user = user_obj.user
                results_date.append(f'{datetime.strftime(period_start, "%d/%m/%Y")} - '
                                    f'{datetime.strftime(period_end, "%d/%m/%Y")}')
                results_usernames.append(user.username)
                results_minutes_in_voice_channels.append(str(user_activity_time))

            embed = Embed(
                title='Summary activity report',
                description='This report shows activity in voice channels.', color=self.report_color)

            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(results_date), inline=True)
            embed.add_field(name=MEMBER_COLUMN_NAME, value='\n'.join(
                results_usernames), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(results_minutes_in_voice_channels)),
                            inline=True)

            return await interaction.response.send_message(embed=embed)

        async def everyone_activity_lasts_btn_callback(interaction):
            user_activity = session.query(UserActivityModel).order_by(
                UserActivityModel.date.desc(),
                UserActivityModel.minutes_in_voice_channels.desc()).limit(25).all()

            if not user_activity:
                return await interaction.response.send_message(
                    'Can`t find anyone activity in the database :(')

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for activity in user_activity:
                results_date.append(datetime.strftime(
                    activity.date, '%d/%m/%Y'))
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(
                    str(activity.minutes_in_voice_channels))

            embed = Embed(
                title='Recent activity report about _Everyone user_',
                description='This report shows activity in voice channels.', color=self.report_color)

            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(results_date), inline=True)
            embed.add_field(name=MEMBER_COLUMN_NAME, value='\n'.join(
                results_usernames), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(results_minutes_in_voice_channels)),
                            inline=True)

            return await interaction.response.send_message(embed=embed)

        today_btn = Button(label='Today', style=ButtonStyle.blurple)
        lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(
            label='Top for all time', style=ButtonStyle.blurple, row=2)
        summary_btn = Button(label='All-time total',
                             style=ButtonStyle.blurple, row=2)

        today_btn.callback = everyone_activity_today_btn_callback
        top_for_all_time_btn.callback = everyone_activity_top_for_all_time_btn_callback
        lasts_btn.callback = everyone_activity_lasts_btn_callback
        summary_btn.callback = everyone_activity_summary_btn_callback

        myview = View(timeout=self.msg_exp_time)
        myview.add_item(today_btn)
        myview.add_item(top_for_all_time_btn)
        myview.add_item(lasts_btn)
        myview.add_item(summary_btn)

        msg_response = await interaction.response.send_message(view=myview)
        await asyncio.sleep(self.msg_exp_time)
        await msg_response.delete()

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def my_activity_callback(self, interaction):
        async def my_activity_lasts_btn_callback(interaction):
            user = session.query(UserModel).filter_by(
                discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = session.query(UserActivityModel).filter_by(user_id=user.id).order_by(
                UserActivityModel.date.desc()).limit(25).all()

            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            for activity in user_activity:
                result[datetime.strftime(
                    activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

            embed = Embed(
                title=f'Recent activity report about _{user.username}_',
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(result.keys()), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

            return await interaction.response.send_message(embed=embed)

        async def my_activity_top_for_all_time_btn_callback(interaction):
            user = session.query(UserModel).filter_by(
                discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = session.query(UserActivityModel).filter_by(user_id=user.id). \
                order_by(UserActivityModel.minutes_in_voice_channels.desc()).limit(
                25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            for activity in user_activity:
                result[datetime.strftime(
                    activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

            embed = Embed(
                title=f'Activity report about _{user.username}_ for all-time',
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(result.keys()), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

            return await interaction.response.send_message(embed=embed)

        async def my_activity_summary_btn_callback(interaction):
            user = session.query(UserModel).filter_by(
                discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = \
                session.query(func.sum(UserActivityModel.minutes_in_voice_channels)).filter_by(
                    user_id=user.id)[0][0]
            user_activity_period_start = session.query(
                UserActivityModel).filter_by(user_id=user.id).first()
            user_activity_period_end = session.query(UserActivityModel).filter_by(user_id=user.id).order_by(
                UserActivityModel.date.desc()).first()

            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            result[f'{datetime.strftime(user_activity_period_start.date, "%d/%m/%Y")} - '
                   f'{datetime.strftime(user_activity_period_end.date, "%d/%m/%Y")}'] = str(user_activity)

            embed = Embed(
                title=f'Summary activity report about _{user.username}_',
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name=DATE_COLUMN_NAME,
                            value='\n'.join(result.keys()), inline=True)
            embed.add_field(name=TIME_COLUMN_NAME, value='\n'.join(self.format_time(result.values())), inline=True)

            return await interaction.response.send_message(embed=embed)

        lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(
            label='Top for all time', style=ButtonStyle.blurple)
        summary_btn = Button(label='All-time total', style=ButtonStyle.blurple)

        lasts_btn.callback = my_activity_lasts_btn_callback
        top_for_all_time_btn.callback = my_activity_top_for_all_time_btn_callback
        summary_btn.callback = my_activity_summary_btn_callback

        myview = View(timeout=self.msg_exp_time)
        myview.add_item(lasts_btn)
        myview.add_item(top_for_all_time_btn)
        myview.add_item(summary_btn)

        msg_response = await interaction.response.send_message(view=myview)
        await asyncio.sleep(self.msg_exp_time)
        await msg_response.delete()

    @nextcord.slash_command(name='activity', description='text description')
    async def activity_voice_channels_check(self, ctx,
                                            user: Member = SlashOption(description="Your number", required=False)):
        await self.bot.wait_until_ready()

        self.ctx = ctx
        self.user_to_check = user

        if isinstance(self.user_to_check, Member):
            try:
                someone_activity_lasts_btn = Button(
                    label='Lasts', style=ButtonStyle.blurple)
                someone_activity_top_for_all_time_btn = Button(
                    label='Top for all time', style=ButtonStyle.blurple)
                someone_activity_summary_btn = Button(
                    label='All-time total', style=ButtonStyle.blurple)

                someone_activity_lasts_btn.callback = self.someone_activity_lasts_btn_callback
                someone_activity_top_for_all_time_btn.callback = self.someone_activity_top_for_all_time_btn_callback
                someone_activity_summary_btn.callback = self.someone_activity_summary_btn_callback

                myview = View(timeout=self.msg_exp_time)
                myview.add_item(someone_activity_lasts_btn)
                myview.add_item(someone_activity_top_for_all_time_btn)
                myview.add_item(someone_activity_summary_btn)

                msg_response = await ctx.send(f'Activity for user **{self.user_to_check.name}**', view=myview)
                await asyncio.sleep(self.msg_exp_time)
                await msg_response.delete()

            except Exception:
                return await ctx.send('The member parameter is incorrect. Select a person as "**@name**"')
        else:

            my_activity_btn = Button(
                label=f'{self.ctx.user.name}\'s activity', style=ButtonStyle.blurple)
            everyones_activity_btn = Button(
                label='Everyone\'s activity', style=ButtonStyle.blurple)

            my_activity_btn.callback = self.my_activity_callback
            everyones_activity_btn.callback = self.everyones_activity_callback

            myview = View(timeout=self.msg_exp_time)
            myview.add_item(my_activity_btn)
            myview.add_item(everyones_activity_btn)

            msg_response = await ctx.send(view=myview)
            await asyncio.sleep(self.msg_exp_time)
            await msg_response.delete()


def register_cog(bot: Bot) -> None:
    bot.add_cog(UserActivity(bot))
