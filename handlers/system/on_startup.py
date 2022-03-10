from discord_bot_wefi.database.db import db_conn
from discord_bot_wefi.loader import bot


@bot.event
async def on_ready():
    print('Starting Bot...')
    if db_conn:
        print('Database connection...OK')
    else:
        print('Database connection...ERROR')
