from settings import engine, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from sqlalchemy import select, insert


async def add_user(user: dict) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(User).values(**user))


async def get_user(id: str) -> list[User]:
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(select(User.id, User.username,
                     User.bio, User.age, User.gender).where(User.id == id))
            return user.first()
        


async def get_users() -> list[User]:
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User))
            return users.all()