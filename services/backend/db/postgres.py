from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import pg_settings

async_engine = create_async_engine(pg_settings.async_dsn, echo=True, future=True)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
) 

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()