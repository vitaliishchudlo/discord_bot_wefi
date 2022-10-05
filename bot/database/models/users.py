from sqlalchemy import Column, Integer, String, BigInteger, INT

from discord_bot_wefi.bot.database.db_init import Base
from sqlalchemy.orm import declarative_base, relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    username = Column(String)
    discriminator = Column(String)

    # activity = relationship('UserActivity', back_populates='user', cascade='all, delete')



    def __repr__(self):
        return f'<User(username={self.username}, discord_id={self.discord_id})>'
