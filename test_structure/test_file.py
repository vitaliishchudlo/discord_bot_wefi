import sys

from models.users import User
from test_structure.database import Session

def go_test():
    session = Session()
    user1 = User(name='John', fullname='Shchudlo')
    session.add(user1)
    session.commit()
