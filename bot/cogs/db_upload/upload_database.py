import os
from logging import getLogger

from nextcord.ext import commands
from nextcord.ext.commands import Bot

from discord_bot_wefi.bot.misc.config import BotLoggerName

logger = getLogger(BotLoggerName)


class UploadDatabaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='upload_db')
    @commands.is_owner()
    async def upload_db_command(self, ctx):
        await self.bot.wait_until_ready()
        logger.info(f'User: {ctx.author} entered the command: "upload_db"')

        # Check if there are attachments to the message
        if len(ctx.message.attachments) == 0:
            logger.info(f'User: {ctx.author} tried to upload the database without attaching a file')
            await ctx.reply("You need to attach a file to the command")
            return

        # Get the first attached file
        attachment = ctx.message.attachments[0]

        # Check the file extension and name
        valid_extensions = (".sqlite", ".db")
        valid_filename = "database"
        file_extension = os.path.splitext(attachment.filename)[1]
        file_name = os.path.splitext(attachment.filename)[0]

        if file_extension not in valid_extensions or file_name != valid_filename:
            logger.info(f'User: {ctx.author} tried to upload an invalid file: {attachment.filename}')
            await ctx.reply(
                "Invalid file. Allowed extensions: **.sqlite**, **.db**. The file name should be **'database'**.")
            return

        # Get the path to the database folder
        database_folder = "bot/database"

        # Check if the database folder exists
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)

        # Save the attached file to the database folder with the original name
        file_path = os.path.join(database_folder, attachment.filename)
        await attachment.save(file_path)

        logger.info(f'User: {ctx.author} successfully uploaded the database: {attachment.filename}')
        await ctx.reply(f"Database successfully uploaded. Path: {file_path}")

    @upload_db_command.error
    async def on_upload_db_command_error(self, ctx, error):
        logger.info(f'Error occurred while executing upload_db command: {error}')
        await ctx.reply('You are not the owner of the Discord server')


def register_cog(bot: Bot) -> None:
    bot.add_cog(UploadDatabaseCog(bot))
