import nextcord
from nextcord import Embed
from nextcord.ext.commands import Bot, Cog


class JsonInfo(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name='json', description='json about server')
    # @commands.command(name='activity')
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


def register_cog(bot: Bot) -> None:
    bot.add_cog(JsonInfo(bot))

# class JsonInfo(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.command()
#     async def json(self, ctx):
#
#         roles = ctx.bot.guilds[0].roles
#         members = ctx.bot.guilds[0].members
#         text_channels = ctx.bot.guilds[0].text_channels
#         voice_channels = ctx.bot.guilds[0].voice_channels
#
#         roles_list = []
#         for role in roles:
#             roles_list.append(f'ID: {role.id} NAME: {role.name}')
#
#         members_list = []
#         for member in members:
#             members_list.append(f'ID: {member.id} NAME: {member.name}')
#
#         text_channels_list = []
#         for text_channel in text_channels:
#             text_channels_list.append(
#                 f'ID: {text_channel.id} NAME: {text_channel.name}')
#
#         voice_channels_list = []
#         for voice_channel in voice_channels:
#             voice_channels_list.append(
#                 f'ID: {voice_channel.id} NAME: {voice_channel.name}')
#
#         await ctx.send(f'**ROLES**\n{chr(10).join(roles_list)}')
#
#         await ctx.send(f'**MEMBERS**\n{chr(10).join(members_list)}')
#
#         await ctx.send(f'**TEXT CHANNELS**\n{chr(10).join(text_channels_list)}')
#
#         return await ctx.send(f'**VOICE CHANNELS**\n{chr(10).join(voice_channels_list)}')
#
#
# def setup(bot):
#     bot.add_cog(JsonInfo(bot))
