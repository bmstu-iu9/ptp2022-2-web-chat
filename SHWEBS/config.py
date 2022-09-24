from pydantic import BaseSettings
"""Файл для получения переменных окружения"""


class Settings(BaseSettings):
    database_url: str = 'postgresql+psycopg2://postgres:1234@localhost/SHWEBS_db'
    app_name: str = 'SHWEBS'


settings = Settings()
