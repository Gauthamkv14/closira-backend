import pytest
from app.core.enums import EnquiryStatus, PriorityLevel


def test_enquiry_full_history_lifecycle(client):
    # 1. Create Enquiry
    payload = {
        "customer_name": "Timeline User",
        "channel": "chat",
        "message": "I need help with my billing and pricing plans please.",
    }
    resp = client.post("/enquiry/", json=payload)
    enquiry_id = resp.json()["enquiry_id"]

    # 2. Schedule Follow-up
    client.post(f"/enquiry/{enquiry_id}/follow-up", json={"delay_minutes": 20})

    # 3. Escalate
    client.post(
        f"/enquiry/{enquiry_id}/escalate",
        json={"escalation_reason": "Manual escalation"},
    )

    # 4. Fetch History
    history_resp = client.get(f"/enquiry/{enquiry_id}/history")
    assert history_resp.status_code == 200
    data = history_resp.json()

    assert data["enquiry_id"] == enquiry_id
    assert data["customer_name"] == "Timeline User"
    assert data["current_status"] == "escalated"
    assert data["priority"] == "high"

    timeline = data["timeline"]
    # Expected events:
    # 1. enquiry_created
    # 2. sop_matched (auto via background task in test client)
    # 3. followup_scheduled
    # 4. escalation_triggered

    event_types = [e["event_type"] for e in timeline]
    assert "enquiry_created" in event_types
    assert "sop_matched" in event_types
    assert "followup_scheduled" in event_types
    assert "escalation_triggered" in event_types

    # Verify chronological ordering (if your history_events relationship uses it)
    # Since we use default append, and created_at timestamps are ascending
    # we should check they are indeed ascending.
    timestamps = [e["timestamp"] for e in timeline]
    assert timestamps == sorted(timestamps)


def test_get_history_not_found(client):
    response = client.get("/enquiry/9999/history")
    assert response.status_code == 404
