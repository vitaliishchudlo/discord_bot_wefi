from logging import getLogger

from nextcord.ext import commands, tasks
from nextcord.ext.commands import Cog, Bot
import requests
from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import UserModel
from discord_bot_wefi.bot.misc.config import BotLoggerName, FACEIT_API_BASE_URL, FACEIT_API_KEY, FACEIT_ROLES_BY_LVL

logger = getLogger(BotLoggerName)


class FaceitLvlTracker(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_role_id_depending_on_the_faceit_lvl(self, faceit_lvl):
        role_id = FACEIT_ROLES_BY_LVL.get(f'lvl{faceit_lvl}')
        role_obj = self.bot.guilds[0].get_role(role_id)
        return role_obj if role_obj else None

    @tasks.loop(seconds=360)
    @commands.Cog.listener()
    async def faceit_lvl_check(self, *args):
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
            except Exception:
                pass

        for player in faceit_statistics_result:
            user = session.query(UserModel).filter_by(faceit_player_id=player['player_id']).first()
            user.faceit_elo = player['games']['cs2']['faceit_elo']
            user.faceit_lvl = player['games']['cs2']['skill_level']
            user.faceit_profile_link = player['faceit_url'].replace('{lang}', 'en')
            session.commit()
            logger.info(f'Updating faceit elo for user {user.username} - {user.faceit_elo}/{user.faceit_lvl} lvl')

            discord_user = self.bot.guilds[0].get_member(user.discord_id)
            if discord_user:
                role_obj = await self.get_role_id_depending_on_the_faceit_lvl(user.faceit_lvl)
                await discord_user.add_roles(role_obj)
                logger.info(f'Added role {role_obj} to user {user.username}')

        # ToDo: Bug when trying to get key "cs2" when it`s only csgo:

        """
        "games": {
    "csgo": {
      "region": "EU",
      "game_player_id": "76561198889421960",
      "skill_level": 2,
      "faceit_elo": 950,
      "game_player_name": "andex.qo",
      "skill_level_label": "",
      "regions": {},
      "game_profile_id": ""
    },
    "cs2": {
      "region": "EU",
      "game_player_id": "76561198889421960",
      "skill_level": 4,
      "faceit_elo": 950,
      "game_player_name": "andex.qo",
      "skill_level_label": "",
      "regions": {},
      "game_profile_id": ""
    }
  },
        """


def register_cog(bot: Bot) -> None:
    bot.add_cog(FaceitLvlTracker(bot))
