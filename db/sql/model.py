from sqlalchemy import Column, Integer, BigInteger, Enum, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db.sql.connect import Base
from db.sql.enum.enums import Sex, ChatSettingsSex


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    sex = Column(Enum(Sex), nullable=False, default=Sex.UNKNOWN)
    age = Column(Integer, nullable=False, default=-1)
    is_vip = Column(Boolean, nullable=False, default=False)
    chat_settings = relationship("ChatSettings", back_populates="user", uselist=False)

    def __str__(self):
        return f"ID: {self.id}, \n tg_id: {self.tg_id}, \n sex: {self.sex}, \n age: {self.age}, \n is_vip: {self.is_vip}, \n chat_settings: {self.chat_settings}"


class ChatSettings(Base):
    __tablename__ = 'chat_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sex = Column(Enum(ChatSettingsSex), default=ChatSettingsSex.ANY)
    min_age = Column(Integer, nullable=False, default=0)
    max_age = Column(Integer, nullable=False, default=140)
    user_id = Column(BigInteger, ForeignKey('users.tg_id'), unique=True, nullable=False)
    user = relationship("Users", back_populates="chat_settings")
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_chat_settings'),)

    def __str__(self):
        return f"ID: {self.id}, \n sex: {self.sex}, \n min_age: {self.min_age}, \n max_age: {self.max_age}"


class Connection(Base):
    __tablename__ = 'connection'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_user_id = Column(BigInteger, nullable=False, default=-1)
    second_user_id = Column(BigInteger, nullable=False, default=-1)

    def __str__(self):
        return f"Id {self.id}, \n first_user_id: {self.first_user_id}, \n second_user_id: {self.second_user_id}"

