from fastapi import Depends
from ..dependencies import require_role
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from ..db import get_conn
from ..utils.audit import write_audit   # 🔧 FIX 1: audit logging added
import json
import uuid
import datetime

router = APIRouter(prefix="/evidence", tags=["evidence"])

# =====================================================
# INPUT MODELS (VALIDATION LAYER)
# =====================================================

class GenotypeIn(BaseModel):
    locus: str
    allele1: str
    allele2: str


class EvidenceIn(BaseModel):
    sample_id: Optional[str] = None
    population: Optional[str] = None
    notes: Optional[str] = None
    genotypes: List[GenotypeIn]


# =====================================================
# POST /evidence
# Submit new evidence sample
# =====================================================

@router.post(
    "",
    summary="Submit evidence sample with genotypes"
)
def submit_evidence(
    body: EvidenceIn,
    user=Depends(require_role(["field", "investigator", "admin"]))  
    # 🔧 FIX: capture authenticated user payload (id + role)
):

    # 🔧 FIX 2: prevent empty genotype submission
    if not body.genotypes:
        raise HTTPException(
            status_code=400,
            detail="Evidence must contain at least one genotype"
        )

    evidence_id = str(uuid.uuid4())

    metadata = {
        "sample_id": body.sample_id,
        "population": body.population,
        "notes": body.notes,
        "submitted_at": datetime.datetime.utcnow().isoformat()
    }

    with get_conn() as conn, conn.cursor() as cur:
        try:
            # STEP 1: insert evidence
            cur.execute("""
                INSERT INTO evidence (id, evidence_code, submitted_by, metadata)
                VALUES (%s, %s, %s, %s)
            """, (
                evidence_id,
                body.sample_id or evidence_id,
                user["sub"],  # ✅ FIX: use user ID from JWT payload
                json.dumps(metadata)
            ))

            # STEP 2: insert genotypes with locus validation
            for g in body.genotypes:
                cur.execute(
                    "SELECT id FROM str_loci WHERE locus = %s",
                    (g.locus,)
                )
                locus_row = cur.fetchone()

                if not locus_row:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unknown locus: {g.locus}"
                    )

                cur.execute("""
                    INSERT INTO evidence_genotypes
                    (evidence_id, locus_id, allele1, allele2)
                    VALUES (%s, %s, %s, %s)
                """, (
                    evidence_id,
                    locus_row[0],
                    g.allele1,
                    g.allele2
                ))

            # 🔧 FIX 3: WRITE AUDIT LOG (NEW)
            write_audit(
                cur,
                action="CREATE",
                entity="evidence",
                entity_id=evidence_id,
                details={
                    "sample_id": body.sample_id,
                    "genotypes_count": len(body.genotypes)
                }
            )

            # 🔧 FIX 4: commit everything together
            conn.commit()

        except Exception:
            conn.rollback()   # 🔧 FIX 5: rollback on any failure
            raise

    return {
        "evidence_id": evidence_id,
        "status": "stored"
    }


# =====================================================
# GET /evidence
# List recent evidence
# =====================================================

@router.get(
    "",
    dependencies=[Depends(require_role(["investigator", "admin"]))],
    summary="List recent evidence"
)


def list_evidence(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, evidence_code, received_at, metadata
            FROM evidence
            ORDER BY received_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        return {
            "count": len(rows),
            "items": [
                {
                    "id": str(r[0]),
                    "evidence_code": r[1],
                    "received_at": r[2].isoformat() if r[2] else None,
                    "metadata": json.loads(r[3]) if r[3] else None
                }
                for r in rows
            ]
        }


# =====================================================
# GET /evidence/{evidence_id}
# Get single evidence with genotypes
# =====================================================

@router.get(
    "/{evidence_id}",
    dependencies=[Depends(require_role(["investigator", "admin"]))],
    summary="Get single evidence record"
)
def get_evidence(evidence_id: str):

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, evidence_code, submitted_by, received_at, metadata
            FROM evidence
            WHERE id = %s
        """, (evidence_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Evidence not found")

        cur.execute("""
            SELECT l.locus, eg.allele1, eg.allele2
            FROM evidence_genotypes eg
            JOIN str_loci l ON l.id = eg.locus_id
            WHERE eg.evidence_id = %s
            ORDER BY l.locus
        """, (evidence_id,))

        return {
            "id": str(row[0]),
            "evidence_code": row[1],
            "submitted_by": str(row[2]) if row[2] else None,
            "received_at": row[3].isoformat() if row[3] else None,
            "metadata": json.loads(row[4]) if row[4] else None,
            "genotypes": [
                {"locus": r[0], "allele1": r[1], "allele2": r[2]}
                for r in cur.fetchall()
            ]
        }


# =====================================================
# GET /evidence/{evidence_id}/matches
# =====================================================

@router.get(
    "/{evidence_id}/matches",
    dependencies=[Depends(require_role(["investigator", "admin"]))],
    summary="Get stored matches"
)
def get_evidence_matches(evidence_id: str):

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, profile_id, score, matched_at
            FROM evidence_matches
            WHERE evidence_id = %s
            ORDER BY score DESC NULLS LAST
        """, (evidence_id,))

        rows = cur.fetchall()

        return {
            "count": len(rows),
            "items": [
                {
                    "id": str(r[0]),
                    "profile_id": str(r[1]) if r[1] else None,
                    "score": float(r[2]) if r[2] is not None else None,
                    "matched_at": r[3].isoformat() if r[3] else None
                }
                for r in rows
            ]
        }