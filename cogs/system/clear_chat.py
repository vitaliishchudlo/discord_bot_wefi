import asyncio

from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_any_role

from data import config


class ClearChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @has_any_role(config.ID_ROLE_ADMIN, config.ID_ROLE_MODERATOR, config.ID_ROLE_ACHIEVEMENTS)
    @has_any_role(*config.TEST_LIST)
    async def clear(self, ctx, amount=1):
        defended_chats = config.DEFENDED_CHATS  # ID`s
        if not bool(ctx.channel.id in defended_chats):
            await ctx.message.delete()
            return await ctx.channel.purge(limit=amount)
        author_roles = [role.id for role in ctx.author.roles]
        allowed_roles = config.ID_ROLES_ACHIEVEMENTS_EDITORS
        intersection_roles = list(set(author_roles).intersection(set(allowed_roles)))
        if not intersection_roles:
            msg_bot = await ctx.send("This chat is defended from your role!")
            await asyncio.sleep(1.1)
            await msg_bot.delete()
            return await ctx.message.delete()
        await ctx.message.delete()
        return await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if not isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to use **clear** command!")


def setup(bot):
    bot.add_cog(ClearChat(bot))
