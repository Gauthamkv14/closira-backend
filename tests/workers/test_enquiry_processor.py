from app.workers.enquiry_processor import process_enquiry_task
from app.db.models.enquiry import Enquiry
from app.core.enums import ChannelType, EnquiryStatus, EventType


def test_process_enquiry_task_success(db_session, monkeypatch):
    # 1. Setup: Create an enquiry in the RECEIVED state
    enquiry = Enquiry(
        customer_name="Async Tester",
        channel=ChannelType.CHAT,
        message="I have a question about my pricing.",
    )
    db_session.add(enquiry)
    db_session.commit()
    db_session.refresh(enquiry)

    # 2. Execute
    process_enquiry_task(enquiry.id)
    db_session.refresh(enquiry)

    # 4. Verify
    assert enquiry.status == EnquiryStatus.PROCESSED
    assert enquiry.matched_sop == "Pricing Enquiry"
    assert enquiry.suggested_response is not None

    # Check history (1 for created, 1 for matched)
    # Note: In this test we didn't use the service to create, so we only expect the one from worker
    assert len(enquiry.history_events) == 1
    assert enquiry.history_events[0].event_type == EventType.SOP_MATCHED


def test_process_enquiry_task_escalation(db_session, monkeypatch):
    # Setup message that won't match any SOP
    enquiry = Enquiry(
        customer_name="Escalation Tester",
        channel=ChannelType.EMAIL,
        message="Gibberish random text that matches nothing.",
    )
    db_session.add(enquiry)
    db_session.commit()

    process_enquiry_task(enquiry.id)
    db_session.refresh(enquiry)

    assert enquiry.status == EnquiryStatus.ESCALATED
    assert enquiry.matched_sop == "No Match Found"
    assert len(enquiry.history_events) == 1
    assert enquiry.history_events[0].event_type == EventType.ESCALATED
