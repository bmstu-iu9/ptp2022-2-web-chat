from typing import Tuple

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from hashlib import sha256

from SHWEBS.database import engine, get_session
from SHWEBS import models, schema
from SHWEBS.config import settings


models.Base.metadata.create_all(engine)
app = FastAPI()


@app.post("/token")
async def login(username: str,
                password: str,
        session: Session = Depends(get_session)):
    """Авторизация"""
    hashed_password = sha256(password.encode()).hexdigest()
    user = session.query(models.User).filter_by(username=username).first()


    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    elif user.hashed_password != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid password")

    return user



@app.post("/registration", response_model=schema.User)
async def add_user(username: str,
                   password1: str,
                   password2: str,
                   firstname: str,
                   lastname: str,
                   session: Session = Depends(get_session)):
    """Регистрация"""
    def beautiful_parameters(username: str, firstname: str, lastname: str) -> Tuple[str, str, str]:
        return username.lower(), firstname.lower().capitalize(), lastname.lower().capitalize()

    username, firstname, lastname = beautiful_parameters(username, firstname, lastname)

    if session.query(models.User).filter_by(username=username).count():
        return None
    if password1 != password2:
        return None

    hashed_password = sha256(password1.encode()).hexdigest()

    new_user = models.User(username=username,
                           hashed_password=hashed_password,
                           firstname=firstname,
                           lastname=lastname)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
