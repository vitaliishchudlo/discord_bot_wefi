from sqlalchemy import Column, Integer, String

from discord_bot_wefi.bot.database.db_init import Base


class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return f'<User(name={self.name}, fullname={self.fullname})>'
