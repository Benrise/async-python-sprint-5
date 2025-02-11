import time

from fastapi import APIRouter, Depends
from datetime import datetime

from src.abstract import AsyncCacheStorage
from db.postgres import async_engine
from db.redis import get_cache
from sqlalchemy.future import select

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", summary="Check the availability of services")
async def health_check(cache: AsyncCacheStorage = Depends(get_cache)) -> dict:
    """Проверка доступности приложения, БД и кэша с выводом времени выполнения каждой операции"""

    result = {}

    start_time = time.time()
    result["app"] = {"status": "healthy", "timestamp": datetime.now().isoformat(), "time_ms": (time.time() - start_time) * 1000}
    
    try:
        start_time = time.time()
        async with async_engine.begin() as conn:
            await conn.execute(select(1)) 
        result["db"] = {"status": "ok", "timestamp": datetime.now().isoformat(), "time_ms": (time.time() - start_time) * 1000}
    except Exception as e:
        result["db"] = {"status": "error", "details": str(e), "timestamp": datetime.now().isoformat(), "time_ms": (time.time() - start_time) * 1000}
    
    try:
        start_time = time.time()
        test_key = "health_check"
        test_value = "ok"
        test_expire = 999
        await cache.set(test_key, test_value, test_expire)
        result_cache = await cache.get(test_key)

        if result_cache.decode("utf-8") == test_value:
            result["cache"] = {"status": "ok", "timestamp": datetime.now().isoformat(), "time_ms": (time.time() - start_time) * 1000}
        else:
            raise Exception("Cache value is incorrect")
    except Exception as e:
        result["cache"] = {"status": "error", "details": str(e), "timestamp": datetime.now().isoformat(), "time_ms": (time.time() - start_time) * 1000}

    return result