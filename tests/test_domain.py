import pytest
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from app.db.models.enquiry import Enquiry
from app.db.models.history_event import HistoryEvent
from app.core.enums import ChannelType, EnquiryStatus, EventType
from app.schemas.enquiry import EnquiryCreate
from app.schemas.followup import FollowupCreate


def test_enquiry_model_creation(db_session):
    enquiry = Enquiry(
        customer_name="Alice Smith",
        channel=ChannelType.CHAT,
        message="I need help with my booking",
        status=EnquiryStatus.RECEIVED,
    )
    db_session.add(enquiry)
    db_session.commit()
    db_session.refresh(enquiry)

    assert enquiry.id is not None
    assert enquiry.customer_name == "Alice Smith"
    assert isinstance(enquiry.created_at, datetime)


def test_relationship_enquiry_history(db_session):
    enquiry = Enquiry(
        customer_name="Bob Jones",
        channel=ChannelType.EMAIL,
        message="Complaint about service",
    )
    db_session.add(enquiry)
    db_session.commit()

    event = HistoryEvent(
        enquiry_id=enquiry.id,
        event_type=EventType.CREATED,
        message="Enquiry created from email",
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(enquiry)

    assert len(enquiry.history_events) == 1
    assert enquiry.history_events[0].message == "Enquiry created from email"


def test_enquiry_schema_validation():
    # Valid data
    data = {
        "customer_name": "Jane Doe",
        "channel": "email",
        "message": "This is a long enough message to pass validation.",
    }
    schema = EnquiryCreate(**data)
    assert schema.customer_name == "Jane Doe"

    # Invalid - Too short name
    invalid_data = data.copy()
    invalid_data["customer_name"] = "J"
    with pytest.raises(ValidationError):
        EnquiryCreate(**invalid_data)

    # Invalid - Too short message
    invalid_data = data.copy()
    invalid_data["message"] = "Short"
    with pytest.raises(ValidationError):
        EnquiryCreate(**invalid_data)


def test_followup_schema_validation():
    # Valid
    data = {
        "delay_minutes": 60,
        "template_message": "Checking in",
    }
    schema = FollowupCreate(**data)
    assert schema.delay_minutes == 60
