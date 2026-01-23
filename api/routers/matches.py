from fastapi import APIRouter, HTTPException, Query, Depends
from ..db import get_conn
import uuid
import datetime
from ..dependencies import require_role

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get(
    "/partial/{evidence_id}",
    dependencies=[Depends(require_role(["investigator", "admin"]))],  
    # 🔒 FIX 1: role-based access added
    # Earlier anyone could call this API if dependency was missing
    summary="Partial DNA match against profiles"
)
def partial_match(
    evidence_id: str,
    top: int = Query(20, ge=1, le=200)
):

    with get_conn() as conn, conn.cursor() as cur:

        # ===============================
        # STEP 1: FETCH EVIDENCE GENOTYPES
        # ===============================
        cur.execute("""
            SELECT locus_id, allele1, allele2
            FROM evidence_genotypes
            WHERE evidence_id = %s
        """, (evidence_id,))
        ev_rows = cur.fetchall()

        # 🔧 FIX 2: explicit validation
        # Earlier error message was unclear
        if not ev_rows:
            raise HTTPException(
                status_code=404,
                detail="Evidence not found or no genotypes available"
            )

        loci_ids = [r[0] for r in ev_rows]

        # =====================================
        # 🔧 FIX 3: CLEAR OLD MATCHES
        # =====================================
        # Earlier: repeated calls kept adding duplicate matches
        cur.execute(
            "DELETE FROM evidence_matches WHERE evidence_id = %s",
            (evidence_id,)
        )

        # ===============================
        # STEP 2: MATCH AGAINST PROFILES
        # ===============================
        cur.execute("""
            SELECT p.id, p.sample_id,
                   COUNT(*) FILTER (
                     WHERE
                       (pg.allele1 = ev.allele1 OR pg.allele1 = ev.allele2
                        OR
                        pg.allele2 = ev.allele1 OR pg.allele2 = ev.allele2)
                   ) AS matched_loci,
                   COUNT(*) AS total_loci
            FROM profiles p
            JOIN profile_genotypes pg ON pg.profile_id = p.id
            JOIN evidence_genotypes ev
              ON ev.locus_id = pg.locus_id
             AND ev.evidence_id = %s
            WHERE pg.locus_id = ANY(%s)
            GROUP BY p.id, p.sample_id
            ORDER BY matched_loci DESC
            LIMIT %s
        """, (evidence_id, loci_ids, top))

        rows = cur.fetchall()
        results = []

        # ===============================
        # STEP 3: SCORE + SAVE MATCHES
        # ===============================
        for pid, sid, matched, total in rows:

            # 🔧 FIX 4: skip zero matches
            # Earlier: zero-score profiles were saved
            if matched == 0:
                continue

            # 🔧 FIX 5: safe division
            score = matched / total if total else 0

            # SAVE MATCH
            cur.execute("""
                INSERT INTO evidence_matches
                (id, evidence_id, profile_id, score, matched_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                evidence_id,
                pid,
                round(score, 6),
                datetime.datetime.utcnow()
            ))

            results.append({
                "profile_id": str(pid),
                "sample_id": sid,
                "matched_loci": int(matched),
                "total_loci": int(total),
                "score": round(score, 3)
            })

        # 🔧 FIX 6: commit once after all operations
        conn.commit()

        return {
            "evidence_id": evidence_id,
            "type": "partial",
            "saved_matches": len(results),
            "results": results
        }