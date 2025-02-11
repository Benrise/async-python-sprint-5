from fastapi import APIRouter, Depends
from datetime import datetime

from src.abstract import AsyncCacheStorage
from db.postgres import async_engine
from db.redis import get_cache
from sqlalchemy.future import select

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/app", summary="Check App availability")
async def health_check() -> dict:
    """Проверка доступности приложения"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }

@router.get("/db", summary="Check DB availability")
async def ping() -> dict:
    """Проверка доступности БД"""
    try:
        async with async_engine.begin() as conn:
            await conn.execute(select(1)) 
        return {
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
            }
    except Exception as e:
        return {
                "status": "error", 
                "details": str(e),
                "timestamp": datetime.now().isoformat(),
            }
        
@router.get("/cache", summary="Check Cache availability")
async def ping(cache: AsyncCacheStorage = Depends(get_cache)) -> dict:
    """Проверка доступности кэша"""
    try:
        test_key = "health_check"
        test_value = "ok"
        test_expire = 999
        
        await cache.set(test_key, test_value, test_expire)
        result = await cache.get(test_key)
        
        if result.decode("utf-8") == test_value:
            return {
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise Exception("Cache value is incorrect")
        
    except Exception as e:
        return {
            "status": "error",
            "details": str(e),
            "timestamp": datetime.now().isoformat(),
        }