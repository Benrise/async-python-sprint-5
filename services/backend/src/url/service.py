from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, func

from .utils import generate_short_id
from .models import URL, URLAccess
from .schemas import (
    URLCreateRequest, 
    URLCreateResponse, 
    URLStatusResponse, 
    URLStatusRequest, 
    URLAccessResponse, 
    URLDeleteResponse,
    URLBatchCreateRequest,
    URLBatchCreateResponse
)
from src.config import settings


class URLService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_shorten_url(self, request: URLCreateRequest) -> URLCreateResponse:
        """Создание сокращённого URL"""
        existing_url = await self.db.execute(select(URL).filter(URL.original_url == request.original_url))
        existing_url = existing_url.scalars().first()
        
        if existing_url:
            return URLCreateResponse(short_url_id=existing_url.short_id, short_url=f"{settings.service_url}/{existing_url.short_id}")
        
        short_id = generate_short_id()
        new_url = URL(short_id=short_id, original_url=request.original_url, visibility=request.visibility)
        self.db.add(new_url)
        await self.db.commit()

        return URLCreateResponse(short_url_id=short_id, short_url=f"{settings.service_url}/{short_id}")

    async def batch_create_shorten_url(self, request: URLBatchCreateRequest) -> URLBatchCreateResponse:
        """Создание сокращённых URL-ов пачкой"""
        short_urls = []
        
        for url_request in request.original_urls:
            existing_url = await self.db.execute(select(URL).filter(URL.original_url == url_request.original_url))
            existing_url = existing_url.scalars().first()
            
            if existing_url:
                short_urls.append(URLCreateResponse(short_url_id=existing_url.short_id, short_url=f"{settings.service_url}/{existing_url.short_id}"))
            else:
                short_id = generate_short_id()
                new_url = URL(short_id=short_id, original_url=url_request.original_url, visibility=url_request.visibility)
                self.db.add(new_url)
                await self.db.commit()
                
                short_urls.append(URLCreateResponse(short_url_id=short_id, short_url=f"{settings.service_url}/{short_id}"))
        
        return URLBatchCreateResponse(short_urls=short_urls)

    async def get_url_status(self, short_id: str, request: URLStatusRequest) -> URLStatusResponse:
        """Получение статуса сокращённого URL"""
        result = await self.db.execute(select(URL).filter(URL.short_id == short_id))
        url = result.scalars().first()
        
        if not url:
            raise HTTPException(status_code=404, detail="URL not found")
        
        count_query = select(func.count(URLAccess.id)).filter(URLAccess.url_id == url.id)
        count_result = await self.db.execute(count_query)
        total_count = count_result.scalar() or 0

        accesses_query = (
            select(URLAccess)
            .filter(URLAccess.url_id == url.id)
            .order_by(desc(URLAccess.accessed_at))
            .offset(request.offset)
            .limit(request.max_result)
        )
        accesses_result = await self.db.execute(accesses_query)
        accesses = accesses_result.scalars().all()
        
        if request.full_info:
            accesses_list = [
                URLAccessResponse(
                    accessed_at=access.accessed_at,
                    client_info=access.client_info
                )
                for access in accesses
            ]
        else:
            accesses_list = [
                URLAccessResponse(
                    accessed_at=access.accessed_at
                )
                for access in accesses
            ]
        
        return URLStatusResponse(
            short_url=f"{settings.service_url}/{url.short_id}",
            total_accesses=total_count,
            accesses=accesses_list
        )

    async def delete_url(self, short_id: str) -> URLDeleteResponse:
        """Удаление сокращённого URL (помечается как удалённый)"""
        url = await self.db.execute(select(URL).filter(URL.short_id == short_id))
        url = url.scalars().first()

        if not url:
            raise HTTPException(status_code=404, detail="URL not found")
        
        url.is_deleted = True
        self.db.add(url)
        await self.db.commit()

        return URLDeleteResponse(status="success", message="URL marked as deleted")