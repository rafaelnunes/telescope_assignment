"""Health API Endpoints"""

from api.deps import DBSession
from core.config import settings
from fastapi import APIRouter, HTTPException
from sqlmodel import select, text


router = APIRouter(tags=["health"])


@router.get("/health")
async def health(db_session: DBSession):
    try:
        # Check if the database is reachable
        await db_session.exec(select(text("1")))
    except Exception:
        raise HTTPException(status_code=500, detail="API is not healthy")
    return {
        "status": "ok",
        "version": settings.VERSION,
    }
