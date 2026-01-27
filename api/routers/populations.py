from logging import getLogger
from fastapi import APIRouter, Depends
from ..db import get_conn
from ..dependencies import require_role

logger = getLogger("dna-api")

router = APIRouter(prefix="/populations", tags=["populations"])

@router.get("")
def list_populations(
    user=Depends(require_role(["admin", "investigator"]))
):
    # ✅ LOG FIRST
    logger.info("Fetching populations from database")

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name FROM populations ORDER BY name")
        data = [{"id": i, "name": n} for i, n in cur.fetchall()]

    return data