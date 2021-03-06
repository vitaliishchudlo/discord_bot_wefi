from discord.ext import commands


class JsonInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def json(self, ctx):

        roles = ctx.bot.guilds[0].roles
        members = ctx.bot.guilds[0].members
        text_channels = ctx.bot.guilds[0].text_channels
        voice_channels = ctx.bot.guilds[0].voice_channels

        roles_list = []
        for role in roles:
            roles_list.append(f'ID: {role.id} NAME: {role.name}')

        members_list = []
        for member in members:
            members_list.append(f'ID: {member.id} NAME: {member.name}')

        text_channels_list = []
        for text_channel in text_channels:
            text_channels_list.append(
                f'ID: {text_channel.id} NAME: {text_channel.name}')

        voice_channels_list = []
        for voice_channel in voice_channels:
            voice_channels_list.append(
                f'ID: {voice_channel.id} NAME: {voice_channel.name}')

        await ctx.send(f'**ROLES**\n{chr(10).join(roles_list)}')

        await ctx.send(f'**MEMBERS**\n{chr(10).join(members_list)}')

        await ctx.send(f'**TEXT CHANNELS**\n{chr(10).join(text_channels_list)}')

        return await ctx.send(f'**VOICE CHANNELS**\n{chr(10).join(voice_channels_list)}')


def setup(bot):
    bot.add_cog(JsonInfo(bot))
