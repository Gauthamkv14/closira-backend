from pydantic import BaseModel, Field


class EscalationRequest(BaseModel):
    reason: str = Field(
        ...,
        min_length=5,
        examples=["Customer is very unhappy", "Complex technical issue"],
    )
