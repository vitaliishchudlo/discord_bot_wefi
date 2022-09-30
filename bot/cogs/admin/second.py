from nextcord.ext.commands import Cog, Bot


# todo: AdminCogs
class __MainAdminSecondCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot


def register_admin_cogs(bot: Bot) -> None:
    print('admin2')
    bot.add_cog(__MainAdminSecondCog(bot))
