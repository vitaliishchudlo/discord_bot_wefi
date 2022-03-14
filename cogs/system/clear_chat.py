import asyncio

from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_any_role

from data import config


class ClearChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_any_role(config.ACHIVEMENT_ROLE_NAME, config.MODERATOR_ROLE)
    async def clear(self, ctx, amount=1):
        defended_chats = config.DEFENDED_CHATS
        if not bool(ctx.channel.name in defended_chats):
            await ctx.message.delete()
            return await ctx.channel.purge(limit=amount)
        author_roles = [role.name for role in ctx.author.roles]
        allowed_roles = config.ADMINS_ROLES
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
