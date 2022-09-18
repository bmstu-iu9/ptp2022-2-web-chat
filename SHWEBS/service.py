from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *


async def add_user(session: AsyncSession,
                   username: str,
                   hashed_password: str,
                   firstname: str,
                   lastname: str) -> User:

    new_user = User(username=username,
                    hashed_password=hashed_password,
                    firstname=firstname,
                    lastname=lastname)

    session.add(new_user)

    return new_user


async def exist_user(session: AsyncSession,
                     username: str):
    result = await session.execute(select(User).where(User.username == username).limit(1))

    return result.scalars().all()
