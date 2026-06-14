from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.settings import settings

engine = create_async_engine(

    str(settings.pg_dns),
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,
    pool_timeout=5,
    pool_recycle=1800

)

session_factory = async_sessionmaker(

    engine,
    ## after ended session(async session),we can't make query's to DB, so we mark this False
    expire_on_commit=False

)
