from fastapi import APIRouter
from ..db import get_conn

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/health/db")
def health_db():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {
            "status": "ok",
            "db": "connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "db": "disconnected",
            "detail": str(e)
        }