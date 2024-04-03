from logging import getLogger

import requests
from nextcord.ext import tasks
from nextcord.ext.commands import Cog, Bot

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import UserModel
from discord_bot_wefi.bot.misc.config import BotLoggerName, FACEIT_API_BASE_URL, FACEIT_API_KEY, FACEIT_ROLES_BY_LVL

logger = getLogger(BotLoggerName)


class FaceitLvlTracker(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_role_id_depending_on_the_faceit_lvl(self, faceit_lvl):
        """
        Get the required role ID, OBJ and unwanted roles OBJ for the user depending on the faceit lvl
        """
        required_role_id = FACEIT_ROLES_BY_LVL.get(f'lvl{faceit_lvl}')
        required_role_obj = self.bot.guilds[0].get_role(required_role_id)

        unwanted_roles_obj = [self.bot.guilds[0].get_role(role_id) for level, role_id in FACEIT_ROLES_BY_LVL.items() if
                              level != f'lvl{faceit_lvl}']

        return required_role_obj, unwanted_roles_obj

    @tasks.loop(seconds=300)  # Every 5 minutes
    async def faceit_lvl_check(self, *args):
        try:
            await self.bot.wait_until_ready()

            faceit_users = session.query(UserModel).filter(UserModel.faceit_player_id.isnot(None)).all()

            faceit_statistics_result = []
            for user in faceit_users:
                request_url = f'{FACEIT_API_BASE_URL}/players/{user.faceit_player_id}'
                headers = {
                    'accept': 'application/json',
                    'Authorization': f'Bearer {FACEIT_API_KEY}'}
                try:
                    response = requests.get(request_url, headers=headers)
                    if response.status_code == 200:
                        faceit_statistics_result.append(response.json())
                except Exception as err:
                    logger.error(f'[TASK] Something went wrong with request to Faceit servers...\n{err}')

            for player in faceit_statistics_result:
                user = session.query(UserModel).filter_by(faceit_player_id=player['player_id']).first()
                user.faceit_elo = player.get('games', {}).get('cs2', {}).get('faceit_elo',
                                                                             player.get('games', {}).get('csgo',
                                                                                                         {}).get(
                                                                                 'faceit_elo'))
                user.faceit_lvl = player.get('games', {}).get('cs2', {}).get('skill_level',
                                                                             player.get('games', {}).get('csgo',
                                                                                                         {}).get(
                                                                                 'skill_level'))
                user.faceit_profile_link = player['faceit_url'].replace('{lang}', 'en')
                session.commit()
                logger.info(f'[TASK] Faceit profile of user {user.username} - updated! ELO/LVL: {user.faceit_elo}/{user.faceit_lvl}')

                discord_user = self.bot.guilds[0].get_member(user.discord_id)
                if discord_user:
                    required_role_obj, unwanted_roles_obj = await self.get_role_id_depending_on_the_faceit_lvl(
                        user.faceit_lvl)
                    await discord_user.add_roles(required_role_obj)
                    logger.info(f'[TASK] Role: {required_role_obj}; Added to user: {user.username}')
                    for role in unwanted_roles_obj:
                        if role in discord_user.roles:
                            await discord_user.remove_roles(role)
                            logger.info(f'[TASK] Role: {role}; Removed from user {user.username}')
        except Exception as err:
            print(f'[TASK] Error in faceit_lvl_check task: {err}')
            logger.error(f'[TASK] Error in faceit_lvl_check task: {err}')


def register_cog(bot: Bot) -> None:
    bot.add_cog(FaceitLvlTracker(bot))
