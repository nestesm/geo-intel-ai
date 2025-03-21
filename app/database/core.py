from sqlalchemy import  MetaData, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator
import datetime

from settings import settings


class Base(DeclarativeBase):
    type_annotation_map = {
        BIGINT: int,
        datetime.datetime: datetime.datetime,
    }
    metadata = MetaData()

engine = create_async_engine(
    settings.DATABASE_URL_async,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

async_session_maker = sessionmaker(engine, class_=AsyncSession) 

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()