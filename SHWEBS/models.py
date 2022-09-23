from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    hashed_password = Column(String(64), unique=False)
    firstname = Column(String(20), unique=False)
    lastname = Column(String(20), unique=False)
    is_active = Column(Boolean, default=False)
