from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    firstname: str
    lastname: str

    class Config:
        orm_mode = True
