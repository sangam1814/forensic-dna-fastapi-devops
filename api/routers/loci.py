from fastapi import APIRouter, Depends
from ..db import get_conn
from ..dependencies import require_role   # ✅ ADDED

router = APIRouter(prefix="/loci", tags=["loci"])

@router.get("")
def list_loci(
    user = Depends(require_role(["admin", "investigator", "field"]))  # ✅ FIX
):
    # 🔒 JWT required + role check

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, locus FROM str_loci ORDER BY locus")
        return [{"id": i, "locus": l} for i, l in cur.fetchall()]