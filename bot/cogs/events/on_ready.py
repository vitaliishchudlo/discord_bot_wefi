import shutil

from nextcord import Game
from nextcord.ext import commands
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Cog

from discord_bot_wefi.bot.database import session, User
from discord_bot_wefi.bot.misc.util import BColors
from discord_bot_wefi.bot.tasks.runner import start_all_loops


class __OnReady(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def init_users_with_db(self):
        all_members_on_server = [
            member for member in self.bot.get_all_members()]
        all_members_on_database = session.query(User).all()
        all_members_discord_ids_on_database = [
            x.discord_id for x in all_members_on_database]

        for member in all_members_on_server:
            member_model = User(
                discord_id=member.id,
                username=member.name,
                discriminator=member.discriminator
            )
            if member_model.discord_id in all_members_discord_ids_on_database:
                continue
            session.add(member_model)
            session.commit()

        return print(f'Initialization users...{BColors.OKGREEN}{BColors.BOLD}OK{BColors.ENDC}')

    @commands.Cog.listener()
    async def on_ready(self):
        self.init_users_with_db()

        start_all_loops(self.bot)

        columns = shutil.get_terminal_size().columns
        columns = columns // 15 + columns
        print(f'{BColors.BOLD}{BColors.OKGREEN}'
              'The Bot has been successfully launched :-)'
              f'{BColors.ENDC}'.center(columns))

        await self.bot.change_presence(
            activity=Game('Testing'))


def register_cog(bot: Bot) -> None:
    bot.add_cog(__OnReady(bot))
