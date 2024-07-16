from sqlalchemy import Column, Integer, String
from database import Base


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
