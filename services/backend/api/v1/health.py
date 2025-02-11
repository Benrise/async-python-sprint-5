from fastapi import APIRouter
from datetime import datetime

from db.postgres import async_engine
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