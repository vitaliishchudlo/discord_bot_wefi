from discord.ext import commands
from discord.ext.commands import has_any_role, MissingAnyRole

from data import config
from database.db import Database


class Achivements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_any_role(config.ID_OWNER, config.ID_ROLE_ADMIN, config.ID_ROLE_MODERATOR)
    async def refresh(self, ctx):
        response = Database().get_achievement_data()
        response.append((0, 0, 0, 0, 0))
        header = ''
        last_member = response[0][1]
        body = []
        statistic_chat = ctx.bot.get_channel(
            config.ID_CHAT_ACHIEVEMENT_STATISTICS)
        for row in response:
            if last_member == row[1]:
                header = f'╔{"═" * 20}╗\n║{" " * 22}**{row[2]}**\n╠{"═" * 20}╝\n'
                body.append(f'╠═► 🔹[{row[3]}]🔹 ━ {row[4]} ➔ {row[5]}\n║')
                continue
            await statistic_chat.send(f'{header}{chr(10).join(body)}\n╚{"═" * 20}╝\n')
            last_member = row[1]
            header = f'╔{"═" * 20}╗\n║{" " * 22}**{row[2]}**\n╠{"═" * 20}╝\n'
            body.clear()
            body.append(f'╠═► 🔹[{row[3]}]🔹 ━ {row[4]} ➔ {row[5]}\n║')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            return await ctx.send('Sorry, you do not have permissions to do **refresh**')


def setup(bot):
    bot.add_cog(Achivements(bot))
