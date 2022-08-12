from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
"""Файл для соединения с БД"""


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)


Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
