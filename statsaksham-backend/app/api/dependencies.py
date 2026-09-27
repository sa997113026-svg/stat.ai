from typing import Any, Dict, List
from fastapi import Depends, Header, Request, status
from app.core.exceptions import AppError
from app.core.security import decode_access_token
from app.domain.enums import Role
from app.repositories.in_memory import db


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "req-default")


def get_current_user(authorization: str | None = Header(default=None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError(
            code="UNAUTHORIZED",
            message="Missing or invalid Bearer token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id or user_id not in db.users:
        raise AppError(
            code="UNAUTHORIZED",
            message="Authenticated user no longer exists",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return db.users[user_id]


def require_roles(allowed_roles: List[Role]):
    def verifier(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = current_user.get("role")
        if user_role not in allowed_roles and user_role != Role.SUPER_ADMIN:
            raise AppError(
                code="FORBIDDEN",
                message=f"Role '{user_role}' does not have permission for this resource",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return verifier
