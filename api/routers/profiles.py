from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from ..db import get_conn
from ..dependencies import require_role  # 🔧 FIX: Added role-based authorization dependency

router = APIRouter(prefix="/profiles", tags=["profiles"])

# =====================================================
# GET /profiles
# List profiles with filters + pagination
# =====================================================
@router.get("")
def list_profiles(
    q: Optional[str] = Query(None, description="Search by SampleID prefix"),
    population: Optional[str] = Query(None, description="Exact population name"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user=Depends(require_role(["admin", "investigator"]))
    # 🔧 FIX 1:
    # Earlier this endpoint was PUBLIC.
    # Now it requires a valid JWT token AND role must be admin or investigator.
):
    """
    🔒 SECURITY FIX:
    - Removed public access.
    - Only authenticated users with proper roles can list profiles.
    """

    # Build SQL dynamically based on filters
    sql = [
        "SELECT p.id, p.sample_id, pop.name "
        "FROM profiles p "
        "JOIN populations pop ON pop.id = p.population_id"
    ]
    where = []
    params: list = []

    if q:
        where.append("p.sample_id ILIKE %s")
        params.append(q + "%")

    if population:
        where.append("pop.name = %s")
        params.append(population)

    if where:
        sql.append("WHERE " + " AND ".join(where))

    sql.append("ORDER BY p.sample_id LIMIT %s OFFSET %s")
    params.extend([limit, offset])

    query = " ".join(sql)

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, tuple(params))
        rows = cur.fetchall()

        return [
            {"id": r[0], "sample_id": r[1], "population": r[2]}
            for r in rows
        ]


# =====================================================
# GET /profiles/{sample_id}
# Get single profile with genotypes
# =====================================================
@router.get("/{sample_id}")
def get_profile_detail(
    sample_id: str,
    user=Depends(require_role(["admin", "investigator"]))
    # 🔧 FIX 2:
    # Earlier anyone could fetch full DNA genotype data.
    # Now only admin & investigator can access sensitive profile details.
):
    """
    🔒 SECURITY FIX:
    - Protects detailed DNA genotype data.
    - Prevents unauthorized access.
    """

    with get_conn() as conn, conn.cursor() as cur:
        # Fetch profile header
        cur.execute("""
            SELECT p.id, p.sample_id, pop.name
            FROM profiles p
            JOIN populations pop ON pop.id = p.population_id
            WHERE p.sample_id = %s
        """, (sample_id,))
        head = cur.fetchone()

        if not head:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        # Fetch genotypes for the profile
        cur.execute("""
            SELECT l.locus, g.allele1, g.allele2
            FROM profile_genotypes g
            JOIN str_loci l ON l.id = g.locus_id
            WHERE g.profile_id = %s
            ORDER BY l.locus
        """, (head[0],))

        loci = [
            {"locus": r[0], "allele1": r[1], "allele2": r[2]}
            for r in cur.fetchall()
        ]

        return {
            "id": head[0],
            "sample_id": head[1],
            "population": head[2],
            "genotypes": loci
        }