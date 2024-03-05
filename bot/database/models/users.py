from sqlalchemy import Column, Integer, String

from discord_bot_wefi.bot.database.db_init import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    username = Column(String)
    faceit_player_id = Column(String)
    faceit_lvl = Column(Integer)
    faceit_elo = Column(Integer)
    faceit_profile_link = Column(String)

    # Can be used this method of the relationship. But used method in models/users_activity.py
    # Part 1
    # activity = relationship('UserActivity', back_populates='user', cascade='all, delete')

    def __repr__(self):
        return f'<{self.__class__.__name__}(username={self.username}, discord_id={self.discord_id})>'
