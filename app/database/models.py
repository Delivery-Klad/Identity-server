from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean

from app.database.database import DataBase


class Users(DataBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(90), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    email = Column(String(300), nullable=True)
    alt_name = Column(String(150), nullable=True)
    description = Column(String(300), nullable=True)
    image_url = Column(String(300), nullable=True)
    status = Column(Boolean, nullable=False)
    pubkey = Column(Text, nullable=True)
    theme = Column(String(10), nullable=False)
    badges = Column(Text, nullable=True)
    about = Column(String(300), nullable=True)


class Messages(DataBase):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey("users.id"))
    target = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    read = Column(Boolean)
    edited = Column(Boolean)
    attachment = Column(String(20), nullable=True)
    date = Column(DateTime)
    reply_id = Column(Integer, nullable=True)


class GroupsMessages(DataBase):
    __tablename__ = "groups_messages"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    sender = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    edited = Column(Boolean)
    attachment = Column(String(20), nullable=True)
    service = Column(Boolean, nullable=True)
    date = Column(DateTime)
    reply_id = Column(Integer, nullable=True)


class Attachment(DataBase):
    __tablename__ = "attachment"
    id = Column(Integer, primary_key=True)
    type = Column(String(30))
    name = Column(Text)
    url = Column(Text)
    height = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)


class ChatKeys(DataBase):
    __tablename__ = "chat_keys"
    id = Column(Integer, primary_key=True)
    user1 = Column(Integer, ForeignKey("users.id"))
    user2 = Column(Integer, ForeignKey("users.id"))
    key1 = Column(Text)
    key2 = Column(Text)


class Groups(DataBase):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    owner = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String(300), nullable=True)


class Members(DataBase):
    __tablename__ = "members"
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    key = Column(Text, nullable=False)


class Posts(DataBase):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    text = Column(Text, nullable=False)
