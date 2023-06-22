import os

from nextcord.ext import commands
from nextcord.ext.commands import Bot


class UploadDatabaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='upload_db')
    @commands.is_owner()
    async def upload_db_command(self, ctx):
        # Перевірка, чи є прикріплення до повідомлення
        if len(ctx.message.attachments) == 0:
            await ctx.reply("You need to attach a file to the command")
            return

        # Отримання першого прикріпленого файлу
        attachment = ctx.message.attachments[0]

        # Перевірка розширення та імені файлу
        valid_extensions = (".sqlite", ".db")
        valid_filename = "database"
        file_extension = os.path.splitext(attachment.filename)[1]
        file_name = os.path.splitext(attachment.filename)[0]

        if file_extension not in valid_extensions or file_name != valid_filename:
            await ctx.reply(
                "Invalid file. Allowed extensions: **.sqlite**, **.db**. The file name should be **'database'**.")
            return

        # Отримання шляху до папки бази даних
        database_folder = "bot/database"

        # Перевірка, чи існує папка бази даних
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)

        # Збереження прикріпленого файлу в папку бази даних зі збереженням оригінального імені
        file_path = os.path.join(database_folder, attachment.filename)
        await attachment.save(file_path)

        await ctx.reply(f"DataBase successfully uploaded. Path:{file_path}")

    @upload_db_command.error
    async def on_upload_db_command_error(self, ctx, error):
        await ctx.reply('You are not owner of the discord server')


def register_cog(bot: Bot) -> None:
    bot.add_cog(UploadDatabaseCog(bot))
