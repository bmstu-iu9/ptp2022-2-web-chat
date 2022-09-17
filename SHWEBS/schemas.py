from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    firstname: str
    lastname: str
    active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
