import os
from logging import getLogger
from pathlib import Path

import nextcord
from nextcord import Embed
from nextcord import File
from nextcord import SlashOption
from nextcord.ext.commands import Bot, Cog

from discord_bot_wefi.bot.misc.config import BotLoggerName

logger = getLogger(BotLoggerName)


class LogsInfo(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logs_dir = f'{Path().absolute()}/logs'

    def get_list_of_logs_files(self, list_of_ids=None):
        if list_of_ids:
            return len(sorted(os.listdir(self.logs_dir), reverse=True))
        return sorted(os.listdir(self.logs_dir), reverse=True)

    @nextcord.slash_command(name='get_logs', description='Get logs files.')
    async def get_logs(self, ctx,
                       log_file_target: int = SlashOption(description="File ID. /logs_show -> list of files id",
                                                          required=True)):
        await self.bot.wait_until_ready()
        log_file_needed = None

        if log_file_target > 0 and self.get_list_of_logs_files(list_of_ids=True) >= log_file_target > 0:
            logs_files = self.get_list_of_logs_files()
            log_file_needed = logs_files[log_file_target - 1]
            response_file = File(f'{self.logs_dir}/{log_file_needed}')
            logger.info(
                f'User: {ctx.user.name} entered the command :"get_logs" with parameter: {log_file_target} (log file name: {log_file_needed})')
            if log_file_target - 1 == 0:
                return await ctx.send(f'Log file for **today**', file=response_file)
            return await ctx.send(f'Log file for **{log_file_needed.split(".")[1]}**', file=response_file)
        else:
            logs_files = self.get_list_of_logs_files()
            for file in logs_files:
                if 'bot_logs.' in file:
                    file.replace('bot_logs.', '')
                if '.log' in file:
                    file.replace('.log', '')
            embed_list_files = Embed()
            embed_list_files.title = 'Chosen bad ID. You can enter next ID`s:'

            embed_list_files.add_field(name='№', value='\n'.join([str(x) for x in range(1, len(logs_files) + 1)]),
                                       inline=True)
            embed_list_files.add_field(name='File', value='\n'.join(logs_files), inline=True)

            logger.info(f'User: {ctx.user.name} entered the command :"get_logs" with bad parameter: {log_file_target}')

            return await ctx.send(embed=embed_list_files)

    @nextcord.slash_command(name='logs_show', description='Information about available files of logs')
    async def logs_info(self, ctx):
        await self.bot.wait_until_ready()
        self.ctx = ctx

        logs_files = self.get_list_of_logs_files()
        for file in logs_files:
            if 'bot_logs.' in file:
                file.replace('bot_logs.', '')
            if '.log' in file:
                file.replace('.log', '')

        # TODO: replace this  in the files for economy place.
        embed_list_files = Embed()

        embed_list_files.add_field(name='№', value='\n'.join([str(x) for x in range(1, len(logs_files) + 1)]),inline=True)
        embed_list_files.add_field(name='File', value='\n'.join(logs_files), inline=True)

        logger.info(f'User: {self.ctx.user.name} entered the command :"logs_show"')

        await ctx.send(embed=embed_list_files)


def register_cog(bot: Bot) -> None:
    bot.add_cog(LogsInfo(bot))
