from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict
from app.core.enums import EventType


class HistoryEventBase(BaseModel):
    event_type: EventType
    message: str
    metadata_json: Dict[str, Any] | None = None


class HistoryEventInDB(HistoryEventBase):
    id: int
    enquiry_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoryEventResponse(HistoryEventInDB):
    pass
