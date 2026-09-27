import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from app.core.config import settings
from app.core.exceptions import AppError
from fastapi import status


def hash_password(password: str) -> str:
    salt = "statsaksham-pbkdf2-salt"
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return dk.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    expected = hash_password(plain_password)
    return hmac.compare_digest(expected, hashed_password)


def create_access_token(subject: str, role: str, department_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
        "department_id": department_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise AppError(
            code="AUTHENTICATION_FAILED",
            message="Invalid or expired authentication token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from exc
