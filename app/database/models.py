from sqlalchemy import Column, Integer, String, Text, Boolean

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
