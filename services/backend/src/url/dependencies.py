from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from service import URLService
from db.postgres import get_async_session

async def get_url_service(db: AsyncSession = Depends(get_async_session)) -> URLService:
    """Возвращает экземпляр URLService для использования в роутах."""
    return URLService(db)