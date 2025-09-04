from sqlalchemy import create_engine, Column, Integer, String, update, case, select, insert, exists, delete, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import *
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine, AsyncSession

import asyncio
from contextlib import asynccontextmanager

from Card_Name_Platform_Service.orm_sqlalchemy.table.Account_Info import *

class SQLAlchemy_Postgres():
    db_url: str
    engine: Engine
    base: object
    #async_session = None

    def async_session_generator(autocommit: bool):
        if autocommit:
            return sessionmaker(SQLAlchemy_Postgres.engine, class_=AsyncSession)
        else:
            return sessionmaker(SQLAlchemy_Postgres.engine, class_=AsyncSession, autocommit=False)

    @asynccontextmanager
    async def get_session(autocommit=True):
        session = None
        try:
            async_session = SQLAlchemy_Postgres.async_session_generator(autocommit=autocommit)
            async with async_session() as session:
                yield session
        except Exception as e:
            if session:
                await session.rollback()
            raise ValueError(e)
        finally:
            await session.close()



def load_settings_sqlalchemy(DB_HOST, DB_PORT, USERNAME, PASSWORD, DB_NAME, DB_ENGINE_TYPE="postgres"):
    if(DB_ENGINE_TYPE == "postgres"):
        SQLAlchemy_Postgres.db_url = "postgresql+asyncpg://" + USERNAME + ":" + PASSWORD + "@" + DB_HOST + ":" + str(DB_PORT) + "/" + DB_NAME
        SQLAlchemy_Postgres.engine = create_async_engine(url=SQLAlchemy_Postgres.db_url, echo=False, future=True)
        SQLAlchemy_Postgres.base = declarative_base()
        #SQLAlchemy_Postgres.async_session = async_sessionmaker(bind=SQLAlchemy_Postgres.engine, expire_on_commit=False)

