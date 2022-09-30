from nextcord.ext.commands import Cog, Bot
import os


# todo: AdminCogs
class __OnMemberJoin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.bot.get_channel(config.ID_CHAT_WELCOME)
        if not welcome_channel:
            return print('Welcome channel not entered!')
        if not os.path.isdir('captchas'):
            os.mkdir('captchas')
        captcha_picture = generate_captcha(member.id, member.name)
        await welcome_channel.send(
            f'👋 Hello, {member.mention}. Welcome to the We-Fi server!\n'
            f'You need to register. '
            f'Please, enter:  **{config.BOT_PREFIX}register** __captcha__',
            file=captcha_picture)


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__OnMemberJoin(bot))
