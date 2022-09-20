from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from discord_bot_wefi.bot.misc import config as conf


engine = create_engine(f'sqlite:///{conf.PATH_DATABASE}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
