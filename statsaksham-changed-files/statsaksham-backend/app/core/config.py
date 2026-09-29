import json
import os
from typing import List
from pydantic import BaseModel


def _cors_origins() -> List[str]:
    """Localhost + the deployed Vercel site, plus anything in the CORS_ORIGINS env var
    (JSON list or comma-separated). Without this the Vercel site is blocked by CORS and
    silently falls back to mock data."""
    defaults = ["http://localhost:3000", "http://127.0.0.1:3000", "https://stat-ai.vercel.app"]
    raw = os.getenv("CORS_ORIGINS", "").strip()
    extra: List[str] = []
    if raw:
        try:
            parsed = json.loads(raw)
            extra = parsed if isinstance(parsed, list) else [str(parsed)]
        except json.JSONDecodeError:
            extra = [o.strip() for o in raw.split(",") if o.strip()]
    return list(dict.fromkeys(defaults + [str(o).rstrip("/") for o in extra]))


class Settings(BaseModel):
    APP_NAME: str = "StatSaksham AI Backend API"
    APP_VERSION: str = "2.4.0"
    APP_ENV: str = os.getenv("APP_ENV", "demo")
    APP_MODE: str = os.getenv("APP_MODE", "demo")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-only-ephemeral-secret-key-change-in-prod")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-only-jwt-secret-key-change-in-prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./statsaksham_demo.db")
    CORS_ORIGINS: List[str] = _cors_origins()
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
    IGOT_API_BASE_URL: str = os.getenv("IGOT_API_BASE_URL", "https://mock.igot.local")
    NSSTA_API_BASE_URL: str = os.getenv("NSSTA_API_BASE_URL", "https://mock.nssta.local")
    TPAC_API_BASE_URL: str = os.getenv("TPAC_API_BASE_URL", "https://mock.tpac.local")
    FILE_STORAGE_PROVIDER: str = os.getenv("FILE_STORAGE_PROVIDER", "local")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Configurable Proficiency Thresholds (Never hardcoded deep inside business logic)
    LEVEL_UPGRADE_SCORE_THRESHOLD: float = 75.0


settings = Settings()
