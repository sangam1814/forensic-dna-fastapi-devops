from logging import getLogger
from fastapi import APIRouter, Depends, Query
from ..db import get_conn
from ..dependencies import require_role

logger = getLogger("dna-api")

router = APIRouter(prefix="/populations", tags=["populations"])

@router.get("")
def list_populations(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user=Depends(require_role(["admin", "investigator"]))
):
    with get_conn() as conn, conn.cursor() as cur:

        cur.execute("SELECT COUNT(*) FROM populations")
        total = cur.fetchone()[0]

        cur.execute(
            "SELECT id, name FROM populations ORDER BY name LIMIT %s OFFSET %s",
            (limit, offset)
        )
        rows = cur.fetchall()

    return {
        "items": [{"id": i, "name": n} for i, n in rows],
        "total": total
    }