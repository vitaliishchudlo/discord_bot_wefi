from sqlalchemy import event, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from discord_bot_wefi.bot.misc import config as conf
from discord_bot_wefi.bot.misc.util import BColors

engine = create_engine(f'sqlite:///{conf.PATH_DATABASE}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


@event.listens_for(Base.metadata, 'after_create')
def receive_after_create(target, connection, tables, **kw):
    "listen for the 'after_create' event"
    print(f'{BColors.BOLD}Running migrations:{BColors.ENDC}')
    if tables:
        for x in tables:
            print(
                f'    Applying table: {x.name}...{BColors.OKGREEN}OK{BColors.ENDC}')
    else:
        print(f'{BColors.WARNING}    All migrations is up to date!{BColors.ENDC}')


def create_db():
    Base.metadata.create_all(engine)
