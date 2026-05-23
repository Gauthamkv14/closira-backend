from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import EventType, EnquiryStatus, PriorityLevel, ChannelType


class TimelineEventResponse(BaseModel):
    """
    Representation of a single audit event in the enquiry lifecycle.
    """

    event_type: str = Field(..., description="The type of event that occurred")
    message: str = Field(..., description="Human-readable description of the activity")
    timestamp: datetime = Field(
        ..., validation_alias="created_at", description="When the event occurred"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, validation_alias="metadata_json", description="Event-specific payload"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EnquiryHistoryResponse(BaseModel):
    """
    Full CRM-style activity timeline for a customer enquiry.
    """

    enquiry_id: int = Field(..., validation_alias="id")
    customer_name: str
    channel: ChannelType
    current_status: EnquiryStatus = Field(..., validation_alias="status")
    priority: PriorityLevel
    created_at: datetime

    # Enrichment fields
    matched_sop: Optional[str] = None
    suggested_response: Optional[str] = None

    # The actual timeline
    timeline: List[TimelineEventResponse] = Field(
        ..., validation_alias="history_events"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
