import typer
import asyncio

from typing import Tuple

from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

from starlette import status as st

from sqlalchemy.ext.asyncio import AsyncSession

from hashlib import sha256

from SHWEBS.database import engine, get_session, init_models
from SHWEBS.config import settings
from SHWEBS.exceptions import DuplicatedUserError
from SHWEBS import models, schemas
from SHWEBS import service


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/")
async def home(request: Request):
    """Главная страница"""
    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'app_name': settings.app_name,
        }
    )


@app.post("/token")
async def login(username: str,
                password: str,
        session: AsyncSession = Depends(get_session)):
    """Авторизация"""
    hashed_password = sha256(password.encode()).hexdigest()
    user = session.query(models.User).filter_by(username=username).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    elif user.hashed_password != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid password")

    return user


@app.get("/registration")
async def registration(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse(
        'registration.html',
        {
            'request': request,
            'app_name': settings.app_name,
        }
    )


@app.post("/registration", response_model=schemas.User)
async def add_user(username: str,
                   password1: str,
                   password2: str,
                   firstname: str,
                   lastname: str,
                   session: AsyncSession = Depends(get_session)):
    """Регистрация"""
    def beautiful_parameters(username: str,
                             firstname: str,
                             lastname: str) -> Tuple[str, str, str]:
        return username.lower(), firstname.lower().capitalize(), lastname.lower().capitalize()

    username, firstname, lastname = beautiful_parameters(username, firstname, lastname)

    if service.exist_user(session=session, username=username):
        return None
    if password1 != password2:
        return None

    hashed_password = sha256(password1.encode()).hexdigest()
    new_user = service.add_user(session=session,
                                username=username,
                                hashed_password=hashed_password,
                                firstname=firstname,
                                lastname=lastname)
    try:
        await session.commit()
        return new_user
    except IntegrityError as e:
        await session.rollback()
        raise DuplicatedUserError("The user exists")


if __name__ == "__main__":
    cli()
