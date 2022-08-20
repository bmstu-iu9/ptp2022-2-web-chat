from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from SHWEBS.database import engine, get_session
from SHWEBS.models import Base


Base.metadata.create_all(engine)
app = FastAPI()


@app.post("/")
async def root(session: Session = Depends(get_session)):
    """Авторизация"""
    raise NotImplementedError


@app.get("/registration")
async def root():
    """Регистрация"""
    raise NotImplementedError


@app.get("/friends")
async def root():
    """Друзья"""
    raise NotImplementedError


@app.get("/messanger")
async def root():
    """Сообщения"""
    raise NotImplementedError
