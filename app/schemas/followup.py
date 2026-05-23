from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class FollowupCreate(BaseModel):
    """
    Request schema for scheduling a customer follow-up.
    """

    delay_minutes: int = Field(
        ...,
        gt=0,
        description="Number of minutes from now to schedule the follow-up",
        examples=[60],
    )
    template_message: Optional[str] = Field(
        None,
        description="Optional custom message to be sent during follow-up",
        examples=["Checking in on your pricing request."],
    )


class FollowupResponse(BaseModel):
    """
    Response schema for a successfully scheduled follow-up.
    """

    id: int = Field(..., description="The unique ID of the follow-up record")
    enquiry_id: int = Field(..., description="The ID of the associated enquiry")
    scheduled_time: datetime = Field(
        ..., description="Timestamp (UTC) when the follow-up is due"
    )
    completed: bool = Field(
        False, description="Whether the follow-up has been performed"
    )
    template_message: Optional[str] = Field(
        None, description="The message that will be sent"
    )

    model_config = ConfigDict(from_attributes=True)
