import pytest
from unittest.mock import patch
from app.services.enquiry_service import EnquiryService
from app.schemas.enquiry import EnquiryCreate
from app.core.enums import ChannelType, EnquiryStatus, EventType


def test_create_enquiry_persistence(db_session):
    enquiry_data = EnquiryCreate(
        customer_name="Marcos Vane",
        channel=ChannelType.EMAIL,
        message="I'm interested in your cloud plans.",
    )

    enquiry = EnquiryService.create_enquiry(db_session, enquiry_data)

    assert enquiry.id is not None
    assert enquiry.customer_name == "Marcos Vane"
    assert enquiry.status == EnquiryStatus.RECEIVED

    # Verify history event was created
    assert len(enquiry.history_events) == 1
    assert enquiry.history_events[0].event_type == EventType.CREATED


def test_create_enquiry_rollback_on_failure(db_session):
    # This is a bit more advanced but we want to ensure atomicity.
    # We'll mock the commit to raise an exception.
    enquiry_data = EnquiryCreate(
        customer_name="Rollback Test",
        channel=ChannelType.CHAT,
        message="This should not be saved",
    )

    # Use standard unittest.mock.patch instead of pytest-mock
    with patch.object(db_session, "commit", side_effect=Exception("DB Failure")):
        with pytest.raises(Exception, match="DB Failure"):
            EnquiryService.create_enquiry(db_session, enquiry_data)

    # Ideally, we verify that the DB was rolled back.
    from app.db.models.enquiry import Enquiry

    results = db_session.query(Enquiry).all()
    assert len(results) == 0
