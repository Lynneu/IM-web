from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, LargeBinary, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# 关联表 for many to many relationship
friendship = Table(
    'friendship',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

# 多对多关系表, 一个聊天室可以有多个用户, 一个用户可以在多个聊天室
chat_users = Table(
    'chat_users',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = Column(String)
    online = Column(Boolean, default=False)

    friends = relationship(
        "User",
        secondary=friendship,
        primaryjoin=id == friendship.c.user_id,
        secondaryjoin=id == friendship.c.friend_id,
        backref="known_by",
    )

    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    chats = relationship("Chat", secondary=chat_users, back_populates="users")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_name = Column(String, index=True)
    chat_type = Column(String, default="private")  # 新添加的字段，标记聊天类型

    messages = relationship("Message", back_populates="chat")
    users = relationship("User", secondary=chat_users, back_populates="chats")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message_type = Column(String)  # text, image, file etc.
    file_data = Column(LargeBinary)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
