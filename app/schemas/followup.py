from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FollowupBase(BaseModel):
    scheduled_time: datetime = Field(..., examples=["2025-05-24T10:00:00Z"])
    template_message: str | None = Field(
        None, examples=["Hello, following up on your enquiry."]
    )


class FollowupCreate(FollowupBase):
    delay_minutes: int | None = Field(
        None, gt=0, description="Optional delay in minutes from now to schedule"
    )


class FollowupInDB(FollowupBase):
    id: int
    enquiry_id: int
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FollowupResponse(FollowupInDB):
    pass
