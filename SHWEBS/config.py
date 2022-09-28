from pydantic import BaseSettings
"""Файл для получения переменных окружения"""


class Settings(BaseSettings):
    database_url: str = 'sqlite:///./sql_app.db'
    app_name: str = 'SHWEBS'
    authjwt_secret_key: str = "secret"


settings = Settings()
