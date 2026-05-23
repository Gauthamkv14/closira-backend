from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import ChannelType, EnquiryStatus, PriorityLevel


class EnquiryBase(BaseModel):
    customer_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Full name of the customer who initiated the enquiry",
        examples=["John Doe"],
    )
    channel: ChannelType = Field(
        ...,
        description="The communication channel through which the enquiry was received",
        examples=[ChannelType.EMAIL],
    )
    message: str = Field(
        ...,
        min_length=10,
        description="The raw message content from the customer",
        examples=["I'm inquiring about your pricing plans for the Pro version."],
    )


class EnquiryCreate(EnquiryBase):
    pass


class EnquiryUpdate(BaseModel):
    status: EnquiryStatus | None = Field(
        None, description="Updated status of the enquiry"
    )
    priority: PriorityLevel | None = Field(
        None, description="Assigned priority level based on content analysis"
    )
    matched_sop: str | None = Field(
        None, description="The name of the standard operating procedure matched"
    )
    suggested_response: str | None = Field(
        None, description="The AI-generated suggested response for the customer"
    )


class EnquiryInDBBase(EnquiryBase):
    id: int
    status: EnquiryStatus
    priority: PriorityLevel
    matched_sop: str | None = None
    suggested_response: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EnquiryResponse(EnquiryInDBBase):
    """Public response for single enquiry."""

    pass
