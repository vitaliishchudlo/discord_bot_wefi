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
            text_channels_list.append(f'ID: {text_channel.id} NAME: {text_channel.name}')

        voice_channels_list = []
        for voice_channel in voice_channels:
            voice_channels_list.append(f'ID: {voice_channel.id} NAME: {voice_channel.name}')

        await ctx.send('**ROLES:**')
        await ctx.send(f'\n'.join(roles_list))

        await ctx.send('**MEMBERS:**')
        await ctx.send(f'\n'.join(members_list))

        await ctx.send('**TEXT CHANNELS:**')
        await ctx.send(f'\n'.join(text_channels_list))

        await ctx.send('**VOICE CHANNELS:**')
        await ctx.send(f'\n'.join(voice_channels_list))



def setup(bot):
    bot.add_cog(JsonInfo(bot))
