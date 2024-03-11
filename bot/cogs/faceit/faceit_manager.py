import re
from logging import getLogger

import nextcord
import requests
from nextcord import SlashOption
from nextcord.ext.commands import Cog, Bot
from nextcord.member import Member

from discord_bot_wefi.bot.database import session
from discord_bot_wefi.bot.database.models.users import UserModel
from discord_bot_wefi.bot.misc.config import BotLoggerName, FACEIT_API_BASE_URL, FACEIT_API_KEY, FACEIT_ROLES_BY_LVL

logger = getLogger(BotLoggerName)


class FaceitManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_role_id_depending_on_the_faceit_lvl(self, faceit_lvl):
        role_id = FACEIT_ROLES_BY_LVL.get(f'lvl{faceit_lvl}')
        role_obj = self.bot.guilds[0].get_role(role_id)
        return role_obj if role_obj else None

    @nextcord.slash_command(name='set_faceit_profile', description='Information about available files of logs')
    async def set_faceit_profile(self, ctx,
                                 faceit_link: str,
                                 command_user: Member = SlashOption(description="Choose user from the server",
                                                                    required=False)):
        await self.bot.wait_until_ready()
        self.ctx = ctx

        if command_user:  # check if the user wants to set faceit profile for other user
            # ctx.user.id != ctx.guild.owner_id - check if the user is not the owner of the server
            if not ctx.permissions.administrator:  # check if the user is not administator
                return await ctx.send('You are not allowed to set faceit profile for other users')

        pattern = re.compile(r'^https?://(?:www\.)?faceit\.com/en/players/(?P<nickname>.+?)(?:/|$)')
        match = pattern.search(faceit_link)
        if not match:
            return await ctx.send('Faceit profile url is invalid')

        faceit_nickname = match.group('nickname')
        request_url = f'{FACEIT_API_BASE_URL}/players'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {FACEIT_API_KEY}'
        }
        params = {
            'nickname': f'{faceit_nickname}',
            'game': '730'
        }

        try:
            response = requests.get(request_url, headers=headers, params=params).json()
            player_id = response['player_id']
            faceit_elo = response.get('games', {}).get('cs2', {}).get('faceit_elo',response.get('games', {}).get('csgo', {}).get('faceit_elo'))
            faceit_lvl = response.get('games', {}).get('cs2', {}).get('skill_level',response.get('games', {}).get('csgo', {}).get('skill_level'))
            faceit_profile_link = response['faceit_url'].replace('{lang}', 'en')
        except Exception:
            return await ctx.send('Something went wrong...')

        if command_user:
            user = session.query(UserModel).filter_by(discord_id=command_user.id).first()
        else:
            user = session.query(UserModel).filter_by(discord_id=ctx.user.id).first()
        user.faceit_player_id = player_id
        user.faceit_elo = faceit_elo
        user.faceit_lvl = faceit_lvl
        user.faceit_profile_link = faceit_profile_link
        session.commit()
        logger.info(f'Updating faceit elo for user {user.username} - {user.faceit_elo}/{user.faceit_lvl} lvl')

        discord_user = self.bot.guilds[0].get_member(user.discord_id)
        if discord_user:
            role_obj = await self.get_role_id_depending_on_the_faceit_lvl(user.faceit_lvl)
            await discord_user.add_roles(role_obj)
            logger.info(f'Added role {role_obj} to user {user.username}')

        return await ctx.send(
            f'User: {user.username}\nFaceit lvl/elo: {user.faceit_lvl}/{user.faceit_elo}\nRole - added')



def register_cog(bot: Bot) -> None:
    bot.add_cog(FaceitManager(bot))
