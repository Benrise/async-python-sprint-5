from fastapi import APIRouter, Depends

from .schemas import (
    URLCreateRequest, 
    URLCreateResponse, 
    URLStatusResponse, 
    URLStatusRequest, 
    URLDeleteResponse,
    URLBatchCreateRequest,
    URLBatchCreateResponse
)

from service import URLService
from dependencies import get_url_service


router = APIRouter(prefix="/url", tags=["URL"])

@router.post("/create", summary="Create shorten version of URL", response_model=URLCreateResponse)
async def create_shorten_url(
    request: URLCreateRequest, 
    url_service: URLService = Depends(get_url_service)
) -> URLCreateResponse:
    """Создание сокращённого URL"""
    return await url_service.create_shorten_url(request)

@router.post("/batch_create", summary="Create multiple shortened URLs in batch", response_model=URLBatchCreateResponse)
async def batch_create_shorten_url(
    request: URLBatchCreateRequest, 
    url_service: URLService = Depends(get_url_service)
) -> URLBatchCreateResponse:
    """Создание сокращённых URL-ов пачкой"""
    return await url_service.batch_create_shorten_url(request)

@router.get(
    "/{short_id}/status",
    summary="Get status of the shortened URL",
    response_model=URLStatusResponse
)
async def get_url_status(
    short_id: str,
    request: URLStatusRequest = Depends(),
    url_service: URLService = Depends(get_url_service)
) -> URLStatusResponse:
    """Получение статуса сокращённого URL"""
    return await url_service.get_url_status(short_id, request)

@router.delete("/{short_id}", summary="Delete URL", response_model=URLDeleteResponse)
async def delete_url(
    short_id: str, 
    url_service: URLService = Depends(get_url_service)
) -> URLDeleteResponse:
    """Удаление сокращённого URL (помечается как удалённый)"""
    return await url_service.delete_url(short_id)