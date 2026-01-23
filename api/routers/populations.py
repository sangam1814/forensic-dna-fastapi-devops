from fastapi import APIRouter, Depends
from ..db import get_conn
from ..dependencies import require_role   # ✅ ADDED

router = APIRouter(prefix="/populations", tags=["populations"])

@router.get("")
def list_populations(
    user = Depends(require_role(["admin", "investigator"]))  # ✅ FIX: JWT + role enforced
):
    # 🔒 Now this API requires:
    # 1. Valid JWT token
    # 2. Role must be admin or investigator

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name FROM populations ORDER BY name")
        return [{"id": i, "name": n} for i, n in cur.fetchall()]