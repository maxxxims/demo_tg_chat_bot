from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase


load_dotenv()
def get_token() -> str:
    return os.getenv('API_TOKEN')
def get_db_url() -> str:
    return os.getenv('DB_URL')


# INIT BOT #
bot = Bot(get_token())
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# INIT DATABASE #
engine = create_async_engine(
    get_db_url(), execution_options={"check_same_thread": False}, future=True, echo=False)                   # , future=True, echo=True
async_session = sessionmaker(expire_on_commit=False, bind=engine, class_=AsyncSession)
# Base = declarative_base()
class Base(DeclarativeBase):
    ...

async def create_tables(*args):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def drop_tables(*args):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


metadata = MetaData()


class Messages:
    start  = 'Привет!\nЭто чат бот для общения на определенные темы. Сначала заполни анекту о себе и выбери тему, которую хотите обсудить.'

