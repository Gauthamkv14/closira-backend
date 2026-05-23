from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import EnquiryStatus


class EscalationCreate(BaseModel):
    """
    Request schema for escalating an enquiry to high priority management review.
    """

    escalation_reason: str = Field(
        ...,
        min_length=10,
        description="Reason for escalating this enquiry",
        examples=[
            "Customer requesting immediate refund",
            "Technical blockage requires senior dev",
        ],
    )


class EscalationResponse(BaseModel):
    """
    Response schema for a successfully escalated enquiry.
    """

    enquiry_id: int = Field(..., description="The ID of the escalated enquiry")
    updated_status: EnquiryStatus = Field(
        ..., description="The new status reflecting escalation"
    )
    escalation_reason: str = Field(
        ..., description="The reason provided for escalation"
    )
    escalated_at: datetime = Field(
        ..., description="Timestamp (UTC) of when the escalation occurred"
    )

    model_config = ConfigDict(from_attributes=True)
