from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from discord_bot_wefi.bot.database.db_init import Base


class UserActivity(Base):
    __tablename__ = 'users_activity'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.strftime(
        datetime.today(), '%d/%m/%Y'), )
    minutes_in_voice_channels = Column(Integer)
    user_id = Column(Integer(), ForeignKey('users.id'))

    # user = relationship('User', back_populates='activity')
    user = relationship('User', backref='activity')

    def __repr__(self):
        return '<UsersActivity(' \
               f'minutes_in_voice_channels={self.minutes_in_voice_channels}, ' \
               f'date={self.date}, ' \
               f'user={self.user})>'
