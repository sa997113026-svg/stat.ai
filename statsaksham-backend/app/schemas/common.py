from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total: int = Field(default=0, ge=0)


class ApiResponse(BaseModel, Generic[T]):
    data: T
    meta: Dict[str, Any] = Field(default_factory=dict)
    request_id: str


class PaginatedApiResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta
    request_id: str
