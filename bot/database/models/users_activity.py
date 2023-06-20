from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from discord_bot_wefi.bot.database.db_init import Base


class UserActivityModel(Base):
    __tablename__ = 'users_activity'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.strftime(
        datetime.today(), '%d/%m/%Y'), )
    minutes_in_voice_channels = Column(Integer)
    user_id = Column(Integer(), ForeignKey('users.id'))

    # Part 2 (from models/users.py)
    # user = relationship('User', back_populates='activity')
    user = relationship('UserModel', backref='activity')

    def __repr__(self):
        return f'<{self.__class__.__name__}(user={self.user}, )>'
