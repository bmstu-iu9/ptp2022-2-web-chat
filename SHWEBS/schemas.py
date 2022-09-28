from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    firstname: str
    lastname: str
    is_active: bool

    class Config:
        orm_mode = True


