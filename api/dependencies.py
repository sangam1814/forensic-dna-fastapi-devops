# api/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

# =============================
# CONFIG
# =============================
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"

security = HTTPBearer()

# =============================
# DECODE TOKEN
# =============================
def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security)
):
    token = creds.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload   # ✅ contains user_id, role
    except JWTError:
        # ✅ FIX: Proper 401 if token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# =============================
# ROLE CHECK
# =============================
def require_role(allowed_roles: list[str]):
    def checker(user=Depends(get_current_user)):
        # ✅ FIX: Role-based access check
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permission"
            )
        return user
    return checker