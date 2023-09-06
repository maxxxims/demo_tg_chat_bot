from settings import engine, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from models.user2user_model import User2User
from sqlalchemy import select, insert, update
from datetime import datetime
from sqlalchemy import func


async def add_user(id: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(User2User).values(id=id, is_searching=False))


async def insert_user_in_expectation(id: str, topic: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(User2User).values(id=id, topic=topic, is_searching=True, companion=None))


async def update_user_in_expectation(id: str, topic: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User2User).values(topic=topic, is_searching=True).where(
                User2User.id == id
            ))

async def stop_user_expectation(id: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User2User).values(is_searching=False).where(
                User2User.id == id))


async def find_companion(id: str, topic: str) -> list[tuple]:
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User2User.id).where(
                User2User.id != id, User2User.topic == topic, User2User.is_searching == True).order_by
                (User2User.start_searching.asc(), User2User.last_activity.asc()).limit(1)
                )
            return users.scalars().all()


async def set_companion(id: str, topic: str, companion: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User2User).values(companion=companion, last_activity=datetime.utcnow(),
                                                           is_searching=False).where(
                User2User.id == id, User2User.topic == topic))
            
            await session.execute(update(User2User).values(companion=id, last_activity=datetime.utcnow(),
                                                           is_searching=False).where(
                User2User.id == companion, User2User.topic == topic))


async def get_companion(id: str) -> str:
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User2User.companion).where(
                User2User.id == id))
            return users.one().companion
        

async def get_user_info(id: str):
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User2User.is_searching, User2User.topic, User2User.companion).where(
                User2User.id == id))
            return users.first()
        

async def stop_dialog(id: str, companion: str) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User2User).values(companion=None, is_searching=False).where(
                User2User.id == id, User2User.companion == companion))
            await session.execute(update(User2User).values(companion=None, is_searching=True).where(
                User2User.id == companion, User2User.companion == id))
            

async def get_users(id: str, topic: str) -> list[tuple]:
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User2User).where(
                User2User.topic == topic, User2User.is_searching == True).order_by
                (User2User.start_searching.asc(), User2User.last_activity.asc())
                )
            return users.scalars().all()
        

async def get_users_by_topics():
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(select(User2User.topic, func.count(User2User.id)).group_by(User2User.topic))
            return users.all()