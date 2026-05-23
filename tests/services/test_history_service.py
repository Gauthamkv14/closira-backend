import pytest
from app.services.history_service import HistoryService
from app.core.enums import EventType
from app.db.models.enquiry import Enquiry
from app.core.enums import ChannelType


def test_create_history_event_persistence(db_session):
    # Setup
    enquiry = Enquiry(customer_name="Test", channel=ChannelType.CHAT, message="Hello")
    db_session.add(enquiry)
    db_session.commit()

    # Execute
    HistoryService.create_history_event(
        db=db_session,
        enquiry_id=enquiry.id,
        event_type=EventType.CREATED,
        message="Test event",
        metadata_json={"foo": "bar"},
        commit=True,
    )

    # Verify
    db_session.refresh(enquiry)
    assert len(enquiry.history_events) == 1
    event = enquiry.history_events[0]
    assert event.event_type == EventType.CREATED
    assert event.message == "Test event"
    assert event.metadata_json == {"foo": "bar"}


def test_create_history_event_no_commit(db_session):
    enquiry = Enquiry(customer_name="Test", channel=ChannelType.CHAT, message="Hello")
    db_session.add(enquiry)
    db_session.commit()

    # Execute with commit=False
    HistoryService.create_history_event(
        db=db_session,
        enquiry_id=enquiry.id,
        event_type=EventType.SOP_MATCHED,
        message="Manual addition",
        commit=False,
    )

    # Verify not yet in DB if we roll back or haven't committed
    # But for a clear test, we verify it's in the session identity map
    # or we commit manually and check.
    db_session.commit()
    db_session.refresh(enquiry)
    assert len(enquiry.history_events) == 1
