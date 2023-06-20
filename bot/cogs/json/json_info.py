from logging import getLogger

import nextcord
from nextcord import Embed
from nextcord.ext.commands import Bot, Cog

from discord_bot_wefi.bot.misc.config import BotLoggerName

logger = getLogger(BotLoggerName)


class JsonInfo(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name='json', description='Return main info about server')
    async def json_info(self, ctx):
        await self.bot.wait_until_ready()
        self.ctx = ctx
        self.guild = self.bot.guilds[0]

        roles_names = [x.name for x in self.guild.roles]
        roles_ids = [str(x.id) for x in self.guild.roles]

        members_names = [x.name for x in self.guild.members]
        members_ids = [str(x.id) for x in self.guild.members]

        text_channels_names = [x.name for x in self.guild.text_channels]
        text_channels_ids = [str(x.id) for x in self.guild.text_channels]

        voice_channels_names = [x.name for x in self.guild.voice_channels]
        voice_channels_ids = [str(x.id) for x in self.guild.voice_channels]

        embed_roles = Embed()
        embed_roles.add_field(
            name='ID', value='\n'.join(roles_ids), inline=True)
        embed_roles.add_field(
            name='Name', value='\n'.join(roles_names), inline=True)

        embed_members = Embed()
        embed_members.add_field(
            name='ID', value='\n'.join(members_ids), inline=True)
        embed_members.add_field(
            name='Name', value='\n'.join(members_names), inline=True)

        embed_text_channels = Embed()
        embed_text_channels.add_field(
            name='ID', value='\n'.join(text_channels_ids), inline=True)
        embed_text_channels.add_field(
            name='Name', value='\n'.join(text_channels_names), inline=True)

        embed_voice_channels = Embed()
        embed_voice_channels.add_field(
            name='ID', value='\n'.join(voice_channels_ids), inline=True)
        embed_voice_channels.add_field(
            name='Name', value='\n'.join(voice_channels_names), inline=True)

        await self.ctx.send(embed=embed_roles)
        await self.ctx.send(embed=embed_members)
        await self.ctx.send(embed=embed_text_channels)
        await self.ctx.send(embed=embed_voice_channels)

        logger.info(f'User: {self.ctx.user.name} entered the command :"json"')

def register_cog(bot: Bot) -> None:
    bot.add_cog(JsonInfo(bot))
