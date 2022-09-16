import asyncio
import os.path

from data import config
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_any_role


class ClearChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._process_config_data()

    def _process_config_data(self):
        current_file_name = os.path.basename(__file__).replace('.py', '')
        cog_values = None

        for cog in config.cogs:
            cog_name = list(cog.keys())[0]
            if '.' in cog_name:
                cog_name = cog_name.split('.')[-1]
            if not cog_name == current_file_name:
                continue
            cog_values = cog.values()

        print(cog_values)
        print(list(cog_values))

        import ipdb; ipdb.set_trace(context=5)





    @commands.command()
    # @has_any_role(*config.TEST_LIST)
    async def clear(self, ctx, amount=1):
        import ipdb; ipdb.set_trace(context=5)




        defended_chats = config.DEFENDED_CHATS  # ID`s
        if not bool(ctx.channel.id in defended_chats):
            await ctx.message.delete()
            return await ctx.channel.purge(limit=amount)
        author_roles = [role.id for role in ctx.author.roles]
        allowed_roles = config.ID_ROLES_ACHIEVEMENTS_EDITORS
        intersection_roles = list(
            set(author_roles).intersection(set(allowed_roles)))
        if not intersection_roles:
            msg_bot = await ctx.send('This chat is defended from your role!')
            await asyncio.sleep(1.1)
            await msg_bot.delete()
            return await ctx.message.delete()
        await ctx.message.delete()
        return await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if not isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to use **clear** cmd!")


def setup(bot):
    bot.add_cog(ClearChat(bot))
