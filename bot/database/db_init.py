# todo: Database engine

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'database.sqlite'
# add database name to config file and replace "name.db"

# engine = create_engine('sqlite:///' + os.getcwd() + '/' + 'database.db',
#                        echo=True)
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
