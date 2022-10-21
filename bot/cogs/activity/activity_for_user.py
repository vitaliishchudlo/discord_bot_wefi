from datetime import datetime

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

    async def someone_activity_lasts_btn_callback(self, interaction):
        await interaction.response.send_message('someone_activity_lasts_btn_callback')

    async def someone_activity_top_for_all_time_btn_callback(self, interaction):
        await interaction.response.send_message('someone_activity_top_for_all_time_btn_callback')

    async def someone_activity_summarly_btn_callback(self, interaction):
        await interaction.response.send_message('someone_activity_summarly_btn_callback')

    async def everyones_activity_callback(self, interaction):
        async def everyone_activity_today_btn_callback(interaction):
            await interaction.response.send_message('everyone_activity_today_btn_callback')

        async def everyone_activity_top_for_all_time_btn_callback(interaction):
            await interaction.response.send_message('everyone_activity_top_for_all_time_btn_callback')

        async def everyone_activity_lasts_btn_callback(interaction):
            await interaction.response.send_message('everyone_activity_lasts_btn_callback')

        async def everyone_activity_summarly_btn_callback(interaction):
            await interaction.response.send_message('everyone_activity_summarly_btn_callback')

        today_btn = Button(label='today', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(label='top', style=ButtonStyle.blurple)
        lasts_btn = Button(label='lasts', style=ButtonStyle.blurple)
        summarly_btn = Button(label='summarly', style=ButtonStyle.blurple)

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

    async def my_activity_callback(self, interaction):
        async def my_activity_lasts_btn_callback(interaction):
            user = session.query(User).filter_by(discord_id=self.ctx.author.id).first()
            if not user:
                return await interaction.response.send_message('Can`t find you in the database. Sorry.')
            user_activity = session.query(UserActivity).filter_by(user_id=user.id).order_by(
                UserActivity.date.desc()).all()[
                            :50]
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
            await interaction.response.send_message('my_activity_top_for_all_time_button_callback')

        async def my_activity_summarly_btn_callback(interaction):
            user = session.query(User).filter_by(discord_id=self.ctx.author.id).first()
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

        lasts_btn = Button(label='lasts', style=ButtonStyle.blurple)
        top_for_all_time_btn = Button(label='TOP for all time', style=ButtonStyle.blurple)
        summarly_btn = Button(label='Summarly for all time', style=ButtonStyle.blurple)

        lasts_btn.callback = my_activity_lasts_btn_callback
        top_for_all_time_btn.callback = my_activity_top_for_all_time_btn_callback
        summarly_btn.callback = my_activity_summarly_btn_callback

        myview = View(timeout=180)
        myview.add_item(lasts_btn)
        myview.add_item(top_for_all_time_btn)
        myview.add_item(summarly_btn)

        await interaction.response.send_message('TEXT HERE', view=myview)

    @commands.command(name='activity')
    async def activity_voice_channels_check(self, ctx, user_to_check=None):
        await self.bot.wait_until_ready()
        self.ctx = ctx

        if user_to_check:
            try:
                self.selected_user_id = user_to_check.replace('@', '').replace('<', '').replace('>', '')

                someone_activity_lasts_btn = Button(label='Lasts', style=ButtonStyle.blurple)
                someone_activity_top_for_all_time_btn = Button(label='Top for all time', style=ButtonStyle.blurple)
                someone_activity_summarly_btn = Button(label='Summarly', style=ButtonStyle.blurple)

                someone_activity_lasts_btn.callback = self.someone_activity_lasts_btn_callback
                someone_activity_top_for_all_time_btn.callback = self.someone_activity_top_for_all_time_btn_callback
                someone_activity_summarly_btn.callback = self.someone_activity_summarly_btn_callback

                myview = View(timeout=180)
                myview.add_item(someone_activity_lasts_btn)
                myview.add_item(someone_activity_top_for_all_time_btn)
                myview.add_item(someone_activity_summarly_btn)

                await ctx.send(f'Activity for user {self.selected_user_id}', view=myview)

            except Exception:
                return self.ctx.reply('The member parameter is incorrect. Select a person as "**@name**"')
        else:

            my_activity_btn = Button(label='My activity', style=ButtonStyle.blurple)
            everyones_activity_btn = Button(label='Everyone\'s activity', style=ButtonStyle.blurple)

            my_activity_btn.callback = self.my_activity_callback
            everyones_activity_btn.callback = self.everyones_activity_callback

            myview = View(timeout=180)
            myview.add_item(my_activity_btn)
            myview.add_item(everyones_activity_btn)

            await ctx.send('lol', view=myview)

        # user = session.query(User).filter_by(discord_id=ctx.author.id).first()
        # if not user:
        #     return await ctx.reply('Can`t find you in the database. Sorry.')
        # user_activity = session.query(UserActivity).filter_by(user_id=user.id).order_by(UserActivity.date.desc()).all()[
        #                 :50]
        # if not user_activity:
        #     return await ctx.reply('Can`t find your activity in the database :(')
        #
        # result = {}
        # for activity in user_activity:
        #     result[datetime.strftime(activity.date, '%d/%m/%Y')] = str(activity.minutes_in_voice_channels)
        #
        # embed = Embed(
        #     title=f"Activity report about _{user.username}_",
        #     description='This report shows activity in voice channels.', color=self.report_color)
        # embed.add_field(name='ㅤㅤDate\ndd/mm/yyyy', value='\n'.join(result.keys()), inline=True)
        # embed.add_field(name='Minutes\nㅤ', value='\n'.join(result.values()), inline=True)
        #
        # await ctx.reply(embed=embed)


def register_cog(bot: Bot) -> None:
    bot.add_cog(__UserActivity(bot))
