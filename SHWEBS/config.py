from pydantic import BaseSettings
"""Файл для получения переменных окружения"""


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://postgresql:palm@5432/postgres'
    app_name: str = 'SHWEBS'


settings = Settings()
