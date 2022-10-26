from datetime import datetime

import nextcord
from nextcord import Color, ButtonStyle, Embed
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from nextcord.ui import Button, View
from sqlalchemy import func

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models import User, UserActivity


class __UserActivity(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.report_color = Color.teal().purple()

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def someone_activity_lasts_btn_callback(self, interaction):
        user = session.query(User).filter_by(discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = session.query(UserActivity).filter_by(user_id=user.id).order_by(
            UserActivity.date.desc()).limit(25).all()

        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        for activity in user_activity:
            result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

        embed = Embed(
            title=f"Activity report about _{user.username}_",
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
        embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

        await interaction.response.send_message(embed=embed)

    async def someone_activity_top_for_all_time_btn_callback(self, interaction):
        user = session.query(User).filter_by(discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = session.query(UserActivity).filter_by(user_id=user.id). \
            order_by(UserActivity.minutes_in_voice_channels.desc()).limit(25).all()
        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        for activity in user_activity:
            result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

        embed = Embed(
            title=f"Activity report about _{user.username}_",
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
        embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

        await interaction.response.send_message(embed=embed)

    async def someone_activity_summarly_btn_callback(self, interaction):
        user = session.query(User).filter_by(discord_id=self.user_to_check.id).first()
        if not user:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} in the database. Sorry.')
        user_activity = \
            session.query(func.sum(UserActivity.minutes_in_voice_channels)).filter_by(user_id=user.id)[0][0]
        user_activity_period_start = session.query(UserActivity).filter_by(user_id=user.id).first()
        user_activity_period_end = session.query(UserActivity).filter_by(user_id=user.id).order_by(
            UserActivity.date.desc()).first()

        if not user_activity:
            return await interaction.response.send_message(
                f'Can`t find {self.user_to_check.name} activity in the database :(')

        result = {}
        result[f'{datetime.strftime(user_activity_period_start.date, "%d/%m/%Y")} - ' \
               f'{datetime.strftime(user_activity_period_end.date, "%d/%m/%Y")}'] = str(user_activity)

        embed = Embed(
            title=f"Activity report about _{user.username}_",
            description='This report shows activity in voice channels.', color=self.report_color)
        embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
        embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

        await interaction.response.send_message(embed=embed)

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def everyones_activity_callback(self, interaction):
        async def everyone_activity_today_btn_callback(interaction):
            today_date = datetime.strptime(datetime.strftime(datetime.today(), '%d/%m/%Y'), '%d/%m/%Y')
            user_activity = session.query(UserActivity).filter_by(date=today_date).limit(25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find activity in the database :(')

            results_usernames = []
            results_minutes_in_voice_channels = []
            for activity in user_activity:
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(str(activity.minutes_in_voice_channels))

            embed = Embed(
                title=f"Activity report about _{datetime.strftime(today_date, '%d/%m/%Y')}_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name='Member\nㅤ', value='\n'.join(results_usernames), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(results_minutes_in_voice_channels), inline=True)

            await interaction.response.send_message(embed=embed)

        async def everyone_activity_top_for_all_time_btn_callback(interaction):
            user_activity = session.query(UserActivity).filter_by().order_by(
                UserActivity.minutes_in_voice_channels.desc()).limit(25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for activity in user_activity:
                results_date.append(datetime.strftime(activity.date, "%d/%m/%Y"))
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(str(activity.minutes_in_voice_channels))

            embed = Embed(
                title=f"Activity report about _EveryOne_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(results_date), inline=True)
            embed.add_field(name='Member\nㅤ', value='\n'.join(results_usernames), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(results_minutes_in_voice_channels), inline=True)

            await interaction.response.send_message(embed=embed)

        async def everyone_activity_summarly_btn_callback(interaction):

            users_activity = session.query(UserActivity).order_by(UserActivity.date.desc()).all()
            users_ids_to_sum = []
            for user_activity in users_activity:
                if not user_activity.user_id in users_ids_to_sum:
                    users_ids_to_sum.append(user_activity.user_id)

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for user_id in users_ids_to_sum:
                user = session.query(User).filter_by(id=user_id).first()
                user_activity = \
                    session.query(func.sum(UserActivity.minutes_in_voice_channels)).filter_by(user_id=user_id)[0][0]
                user_activity_period_start = session.query(func.min(UserActivity.date)).filter_by(
                    user_id=user_id).first()
                user_activity_period_end = session.query(func.max(UserActivity.date)).filter_by(
                    user_id=user_id).order_by(UserActivity.date.desc()).first()
                results_date.append(f'{datetime.strftime(user_activity_period_start[0], "%d/%m/%Y")} - '
                                    f'{datetime.strftime(user_activity_period_end[0], "%d/%m/%Y")}')
                results_usernames.append(user.username)
                results_minutes_in_voice_channels.append(str(user_activity))

            embed = Embed(
                title="Activity report about _Everyone user_",
                description='This report shows activity in voice channels.', color=self.report_color)

            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(results_date), inline=True)
            embed.add_field(name='Member\nㅤ', value='\n'.join(results_usernames), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(results_minutes_in_voice_channels), inline=True)

            await interaction.response.send_message(embed=embed)

        async def everyone_activity_lasts_btn_callback(interaction):

            user_activity = session.query(UserActivity).order_by(UserActivity.date.desc()).limit(25).all()

            if not user_activity:
                return await interaction.response.send_message('Can`t find anyone activity in the database :(')

            results_date = []
            results_usernames = []
            results_minutes_in_voice_channels = []

            for activity in user_activity:
                results_date.append(datetime.strftime(activity.date, '%d/%m/%Y'))
                results_usernames.append(activity.user.username)
                results_minutes_in_voice_channels.append(str(activity.minutes_in_voice_channels))

            embed = Embed(
                title="Activity report about _Everyone user_",
                description='This report shows activity in voice channels.', color=self.report_color)

            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(results_date), inline=True)
            embed.add_field(name='Member\nㅤ', value='\n'.join(results_usernames), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(results_minutes_in_voice_channels), inline=True)

            await interaction.response.send_message(embed=embed)

        today_btn = Button(label='Today', style=ButtonStyle.blurple)
        lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(label='Top for all time', style=ButtonStyle.blurple, row=2)
        summarly_btn = Button(label='All-time total', style=ButtonStyle.blurple, row=2)

        today_btn.callback = everyone_activity_today_btn_callback
        top_for_all_time_btn.callback = everyone_activity_top_for_all_time_btn_callback
        lasts_btn.callback = everyone_activity_lasts_btn_callback
        summarly_btn.callback = everyone_activity_summarly_btn_callback

        myview = View(timeout=180)
        myview.add_item(today_btn)
        myview.add_item(top_for_all_time_btn)
        myview.add_item(lasts_btn)
        myview.add_item(summarly_btn)

        await interaction.response.send_message('TEXT AGAIN', view=myview)

    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    async def my_activity_callback(self, interaction):
        async def my_activity_lasts_btn_callback(interaction):
            user = session.query(User).filter_by(discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = session.query(UserActivity).filter_by(user_id=user.id).order_by(
                UserActivity.date.desc()).limit(25).all()

            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            for activity in user_activity:
                result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

            embed = Embed(
                title=f"Activity report about _{user.username}_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

            await interaction.response.send_message(embed=embed)

        async def my_activity_top_for_all_time_btn_callback(interaction):
            user = session.query(User).filter_by(discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = session.query(UserActivity).filter_by(user_id=user.id). \
                order_by(UserActivity.minutes_in_voice_channels.desc()).limit(25).all()
            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            for activity in user_activity:
                result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)

            embed = Embed(
                title=f"Activity report about _{user.username}_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

            await interaction.response.send_message(embed=embed)

        async def my_activity_summarly_btn_callback(interaction):
            user = session.query(User).filter_by(discord_id=self.ctx.user.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = \
                session.query(func.sum(UserActivity.minutes_in_voice_channels)).filter_by(user_id=user.id)[0][0]
            user_activity_period_start = session.query(UserActivity).filter_by(user_id=user.id).first()
            user_activity_period_end = session.query(UserActivity).filter_by(user_id=user.id).order_by(
                UserActivity.date.desc()).first()

            if not user_activity:
                return await interaction.response.send_message('Can`t find your activity in the database :(')

            result = {}
            result[f'{datetime.strftime(user_activity_period_start.date, "%d/%m/%Y")} - ' \
                   f'{datetime.strftime(user_activity_period_end.date, "%d/%m/%Y")}'] = str(user_activity)

            embed = Embed(
                title=f"Activity report about _{user.username}_",
                description='This report shows activity in voice channels.', color=self.report_color)
            embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
            embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)

            await interaction.response.send_message(embed=embed)

        lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(label='Top for all time', style=ButtonStyle.blurple)
        summarly_btn = Button(label='All-time total', style=ButtonStyle.blurple)

        lasts_btn.callback = my_activity_lasts_btn_callback
        top_for_all_time_btn.callback = my_activity_top_for_all_time_btn_callback
        summarly_btn.callback = my_activity_summarly_btn_callback

        myview = View(timeout=180)
        myview.add_item(lasts_btn)
        myview.add_item(top_for_all_time_btn)
        myview.add_item(summarly_btn)

        await interaction.response.send_message('TEXT HERE', view=myview)

    @nextcord.slash_command(name='activity', description='12345 text description')
    # @commands.command(name='activity')
    async def activity_voice_channels_check(self, ctx, user_to_check=None):
        await self.bot.wait_until_ready()
        self.ctx = ctx
        self.user_to_check = user_to_check
        if user_to_check:
            try:
                self.selected_user_id = int(self.user_to_check.replace('@', '').replace('<', '').replace('>', ''))
                self.user_to_check = self.ctx.guild.get_member(self.selected_user_id)

                someone_activity_lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
                someone_activity_top_for_all_time_btn = Button(label='Top for all time', style=ButtonStyle.blurple)
                someone_activity_summarly_btn = Button(label='All-time total', style=ButtonStyle.blurple)

                someone_activity_lasts_btn.callback = self.someone_activity_lasts_btn_callback
                someone_activity_top_for_all_time_btn.callback = self.someone_activity_top_for_all_time_btn_callback
                someone_activity_summarly_btn.callback = self.someone_activity_summarly_btn_callback

                myview = View(timeout=180)
                myview.add_item(someone_activity_lasts_btn)
                myview.add_item(someone_activity_top_for_all_time_btn)
                myview.add_item(someone_activity_summarly_btn)

                await ctx.send(f'Activity for user {self.user_to_check.name}', view=myview)

            except Exception:
                return await self.ctx.reply('The member parameter is incorrect. Select a person as "**@name**"')
        else:

            my_activity_btn = Button(label=f'{self.ctx.user.name}\'s activity', style=ButtonStyle.blurple)
            everyones_activity_btn = Button(label='Everyone\'s activity', style=ButtonStyle.blurple)

            my_activity_btn.callback = self.my_activity_callback
            everyones_activity_btn.callback = self.everyones_activity_callback

            myview = View(timeout=180)
            myview.add_item(my_activity_btn)
            myview.add_item(everyones_activity_btn)

            await ctx.send('lol', view=myview)


def register_cog(bot: Bot) -> None:
    bot.add_cog(__UserActivity(bot))
