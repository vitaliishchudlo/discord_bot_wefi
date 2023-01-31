from logging import getLogger

from sqlalchemy import event, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from discord_bot_wefi.bot.misc import config as conf
from discord_bot_wefi.bot.misc.config import BotLoggerName
from discord_bot_wefi.bot.misc.util import BColors

logger = getLogger(BotLoggerName)

engine = create_engine(f'sqlite:///{conf.PATH_DATABASE}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


@event.listens_for(Base.metadata, 'after_create')
def receive_after_create(target, connection, tables, **kw):
    """
    listen for the 'after_create' event
    """
    logger.info('Starting migrations...')
    if tables:
        for x in tables:
            logger.info(f'Applying table: {x.name}... OK')
    else:
        logger.warning('All migrations is up to date!')


def create_db():
    Base.metadata.create_all(engine)
