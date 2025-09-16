from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from  app.core.config import settings


async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    pool_size = 5,
    max_overflow = 10,
    echo = True,
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass