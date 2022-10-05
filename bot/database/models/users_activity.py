from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime

from discord_bot_wefi.bot.database.db_init import Base
from sqlalchemy.orm import declarative_base, relationship
from discord_bot_wefi.bot.database.models.users import User

class UserActivity(Base):
    __tablename__ = 'users_activity'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.strftime(datetime.today(), "%d/%m/%Y"),)
    active_minutes = Column(Integer)
    user_id = Column(Integer(), ForeignKey('users.id'))

    # user = relationship('User', back_populates='activity')
    user = relationship('User', backref='activity')




    def __repr__(self):
        return f'<UsersActivity(active_minutes={self.active_minutes}, date={self.date}, user={self.user})>'
