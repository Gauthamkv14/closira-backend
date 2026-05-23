from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["healthy"])
    database: str = Field(..., examples=["connected"])
    timestamp: datetime = Field(..., examples=["2026-05-23T12:45:00Z"])
