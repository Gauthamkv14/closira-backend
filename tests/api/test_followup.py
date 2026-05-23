import pytest
from app.core.enums import ChannelType


def test_schedule_followup_success(client, db_session):
    # 1. Create an enquiry first
    enq_payload = {
        "customer_name": "Followup User",
        "channel": "chat",
        "message": "Testing followups",
    }
    enq_resp = client.post("/enquiry/", json=enq_payload)
    enquiry_id = enq_resp.json()["enquiry_id"]

    # 2. Schedule followup
    follow_payload = {"delay_minutes": 30, "template_message": "Followup msg"}
    response = client.post(f"/enquiry/{enquiry_id}/follow-up", json=follow_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["enquiry_id"] == enquiry_id
    assert data["template_message"] == "Followup msg"
    assert "scheduled_time" in data

    # 3. Verify history event
    from app.db.models.history_event import HistoryEvent
    from app.core.enums import EventType

    event = (
        db_session.query(HistoryEvent)
        .filter(
            HistoryEvent.enquiry_id == enquiry_id,
            HistoryEvent.event_type == EventType.FOLLOWUP_SCHEDULED,
        )
        .first()
    )
    assert event is not None
    assert "followup_id" in event.metadata_json


def test_schedule_followup_invalid_enquiry(client):
    follow_payload = {"delay_minutes": 10}
    response = client.post("/enquiry/9999/follow-up", json=follow_payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_schedule_followup_validation_error(client):
    # delay_minutes must be > 0
    follow_payload = {"delay_minutes": 0}
    response = client.post("/enquiry/1/follow-up", json=follow_payload)
    assert response.status_code == 422
