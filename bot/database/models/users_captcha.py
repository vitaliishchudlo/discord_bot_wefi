from sqlalchemy import Column, Integer, String, BigInteger, INT, Boolean

from discord_bot_wefi.bot.database.db_init import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship


class UserCaptchaModel(Base):
    __tablename__ = 'users_captcha'

    id = Column(Integer, primary_key=True)
    captcha = Column(String)
    captcha_verified = Column(Boolean)
    user_id = Column(Integer(), ForeignKey('users.id'))

    user = relationship('User', backref='captcha')

    def __repr__(self):
        return f'<{self.__class__.__name__}(user={self.user}, captcha_verified={self.captcha_verified},' \
               f'captcha={self.captcha})>'
