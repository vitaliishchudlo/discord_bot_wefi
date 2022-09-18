import sys

from discord_bot_wefi.bot.database.models.users import User
from discord_bot_wefi.bot.database.db_init import Session

def go_test():
    session = Session()
    user1 = User(name='Canny', fullname='Shchudlo')
    session.add(user1)
    session.commit()
