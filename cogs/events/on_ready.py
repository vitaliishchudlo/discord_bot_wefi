from discord.ext import commands
from discord import Game, Activity, ActivityType, Streaming
from data import config
from discord_bot_wefi.database.db import Database

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print('Loading bot...')
        achivement_role = config.ACHIVEMENT_ROLE_NAME
        all_roles = self.bot.guilds[0].roles
        status_role = False
        users = []

        print('\nUpdating users with achivement role...')
        for role in all_roles:
            if achivement_role in role.name:
                status_role = True
        if not status_role:
            # print(f'Starting....Error\nACHIVEMENT_ROLE_NAME - {achivement_role} does not exists\n')
            exit(f'ACHIVEMENT_ROLE_NAME - {achivement_role} does not exists')

        for member in self.bot.guilds[0].members:
            for role in member.roles:
                if str(role) == achivement_role:
                    users.append(member)
                    print(f'**{member.name}** ID({member.id}) - have role "{achivement_role}"')
        print('\n')

        if not Database().reset_sequecne('achivement_users'):
            print('Sequence updating...ERROR')
        print('Sequence updating...SUCCESS')

        if not Database().save_achivement_users(users=users):  # Saving to the DB
            exit('Something happen with DataBase')
        print(f'{len(users)} users have been added to the DB')
        print('\nStarting Bot...SUCCESS\n\n')
        await self.bot.change_presence(activity=Game('Beta version 1.0'))



def setup(bot):
    bot.add_cog(OnReady(bot))
