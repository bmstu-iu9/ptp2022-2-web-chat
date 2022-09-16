from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    firstname: str
    lastname: str
    active: bool

    class Config:
        orm_mode = True
