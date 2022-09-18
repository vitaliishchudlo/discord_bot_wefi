# todo: Database engine
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import base

# add database name to config file and replace "name.db"

engine = create_engine('sqlite:///' + os.getcwd() + '/' + 'database.db',
                       echo=True)
DBSession = sessionmaker(
    binds={
        Base: engine,
    },
    expire_on_commit=False
)

