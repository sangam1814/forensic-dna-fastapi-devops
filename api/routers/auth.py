from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
import datetime
import os
from passlib.context import CryptContext
from ..db import get_conn

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
ALGO = "HS256"

# ✅ SUPPORT BOTH OLD (bcrypt) AND NEW (argon2)
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(body: LoginIn):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT u.id, u.password_hash, r.code
            FROM users u
            JOIN roles r ON r.id = u.role_id
            WHERE u.email = %s
        """, (body.email,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id, password_hash, role = row

        # ✅ SINGLE, CORRECT VERIFICATION
        if not pwd_context.verify(body.password, password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }

        token = jwt.encode(payload, SECRET, algorithm=ALGO)

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": role
        }