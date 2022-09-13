from discord import Game
from discord.ext import commands

from data import config
from database.db import Database

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print('Loading bot...')
        achievement_role_id = str(config.ID_ROLE_ACHIEVEMENTS)
        status_role = False
        users = []

        print('\nChecking roles...OK')
        for role in self.bot.guilds[0].roles:
            if achievement_role_id in str(role.id):
                status_role = True
        if not status_role:
            exit(
                f'Achievement role with ID: {achievement_role_id} - does not exists')

        print('Updating users with achievement role...')
        for member in self.bot.guilds[0].members:
            for role in member.roles:
                if str(role.id) == achievement_role_id:
                    users.append(member)
                    print(
                        f'**{member.name}** ID({member.id}) - have role "{achievement_role_id}"')
        print('\n')

        if not Database().reset_sequecne('achievement_users'):
            print('Sequence updating...ERROR')
        else:
            print('Sequence updating...OK')

        if not Database().save_achivement_users(users=users):  # Saving to the DB
            # exit('Something happen with DataBase')
            print('Something happen with DataBase')
        else:
            print('Updating DataBase...OK')
            print(f'{len(users)} users have been added to the DB')

        print('\nStarting Bot...SUCCESS\n\n')
        await self.bot.change_presence(
            activity=Game(f'{config.VERSION_PREFIX} {config.VERSION_NUBMER}'))


def setup(bot):
    bot.add_cog(OnReady(bot))
