from typing import Tuple
from datetime import datetime, timedelta
from typing import Union

from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from jose import JWTError, jwt
from passlib.context import CryptContext

from starlette import status as st

from sqlalchemy.orm import Session

from hashlib import sha256

from SHWEBS.database import engine, get_session
from SHWEBS import models, schemas
from SHWEBS.config import settings
from SHWEBS.schemas import TokenData

SECRET_KEY = "5c8397d4a3885d6a0f08bed8154edfbf71e203473d6d30e2392779787b8eda51"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(engine)
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/get_user", response_model=schemas.User)
async def get_user(username: str):
    with Session(engine) as session:
        user = session.query(models.User).filter_by(username=username).first()
        if not user:
            return None
        return user


@app.get("/auth_user", response_model=schemas.User)
async def authenticate_user(username: str, password: str):
    hashed_password = sha256(password.encode()).hexdigest()
    user = await get_user(username=username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    if user.hashed_password != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid password")

    return user


@app.get("/users/me", response_model=schemas.User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                session: Session = Depends(get_session)):
    """Авторизация"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    user.active = True
    session.commit()
    session.refresh(user)

    return {"access_token": access_token, "token_type": "bearer"}


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
