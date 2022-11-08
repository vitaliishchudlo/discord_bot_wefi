from sqlalchemy import Column, Integer, String, BigInteger, INT, Boolean

from discord_bot_wefi.bot.database.db_init import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship


class UserCaptchaModel(Base):
    __tablename__ = 'users_captcha'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    verified = Column(Boolean)
    user_id = Column(Integer(), ForeignKey('users.id'))

    user = relationship('UserModel', backref='captcha')

    def __repr__(self):
        return f'<{self.__class__.__name__}(user={self.user}, verified={self.verified},' \
               f'code={self.code})>'
