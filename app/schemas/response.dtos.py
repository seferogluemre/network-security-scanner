from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class BaseResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime = datetime.utcnow()

class ErrorResponse(BaseResponse):
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseResponse):
    success: bool = True
    data: Optional[Any] = None

class PaginatedResponse(SuccessResponse):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool

class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "NetScout API"
    version: str = "2.0.0"
    uptime: Optional[str] = None
    database: str = "connected"
    timestamp: datetime = datetime.utcnow()