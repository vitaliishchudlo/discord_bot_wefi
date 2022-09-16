from data import config


def manage_extensions(bot):
    for cog in config.cogs:
        cog_name = list(cog.keys())[0]
        bot.load_extension(f"cogs.{cog_name}")
