from discord import Member
from discord.ext import commands
from discord.ext.commands import has_any_role, MissingAnyRole, MissingRequiredArgument

from data import config
from database.db import Database


class Achivements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_any_role(config.ID_OWNER, config.ID_ROLE_ADMIN, config.ID_ROLE_MODERATOR)
    async def achi_add(self, ctx, member: Member, game: str, type: str, count: int):
        message = await ctx.send('Updating data...🔄')
        response = Database().update_achievements_data(
            member.id, member.name, game, type, count)
        return await message.edit(
            content='Updating data...✅\n'
                    f'{member.name} - {game} - {type} - **{response}**')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            return await ctx.send('Sorry, you do not have permissions to do that!')
        # Request to the DB to take all the
        if isinstance(error, MissingRequiredArgument):
            # Discord member
            if error.param.name == 'member':
                available_members = Database().get_achievement_users()
                if not available_members:
                    return await ctx.send(
                        'The list of users for whom achievements are available is empty')
                return await ctx.send(
                    f'**Available users:**\n\n{chr(10).join(available_members)}')

            # Game name
            if error.param.name == 'game':
                available_games = Database().get_achievement_games()
                if not available_games:
                    return await ctx.send(
                        'The list of games is empty')
                message = []
                for game in available_games:
                    message.append(
                        f'{game[0]}  -  {game[1]}  -  {game[2]} - {game[3]}')
                await ctx.send('**ID**-**NAME** - **TYPE**  -  **COMMENT**')
                return await ctx.send(chr(10).join(message))

            # Type of the statistic
            if error.param.name == 'type':
                available_games = Database().get_achievement_games()
                if not available_games:
                    return await ctx.send(
                        'The list of games is empty')
                message = []
                selected_game = ctx.args[-1]
                for game in available_games:
                    if not game[1] == selected_game:
                        continue
                    message.append(
                        f'{game[0]}-{game[1]}  -  {game[2]}  -  {game[3]}')
                if not message:
                    return await ctx.send(
                        f'**[ERROR]** - Game "{selected_game}" not found.')
                await ctx.send('**ID**-**NAME** - **TYPE**  -  **COMMENT**')
                return await ctx.send(chr(10).join(message))

            # Count of the amount
            if error.param.name == 'count':
                return await ctx.send('You need to enter **the count** you want to add')

        return await ctx.send(f'**[ERROR]** - {error}')


def setup(bot):
    bot.add_cog(Achivements(bot))
