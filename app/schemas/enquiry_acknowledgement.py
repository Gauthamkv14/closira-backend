from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import EnquiryStatus


class EnquiryAcknowledgement(BaseModel):
    """
    Schema for initial enquiry submission acknowledgement.
    Reflects the asynchronous nature of the processing workflow.
    """

    enquiry_id: int = Field(
        ..., description="The unique identifier allocated to the enquiry"
    )
    status: EnquiryStatus = Field(
        ..., description="Initial lifecycle status", examples=[EnquiryStatus.RECEIVED]
    )
    processing_state: str = Field(
        "queued",
        description="The current state in the async processing pipeline",
        examples=["queued"],
    )
    created_at: datetime = Field(
        ..., description="Timestamp of when the enquiry was accepted"
    )

    model_config = ConfigDict(from_attributes=True)
