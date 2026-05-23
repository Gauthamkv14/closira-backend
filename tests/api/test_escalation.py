from app.core.enums import EnquiryStatus, PriorityLevel


def test_escalate_enquiry_success(client, db_session):
    # 1. Create enquiry
    enq_resp = client.post(
        "/enquiry/",
        json={
            "customer_name": "Esc User",
            "channel": "email",
            "message": "Help me now! I need assistance immediately.",
        },
    )
    enquiry_id = enq_resp.json()["enquiry_id"]

    # 2. Escalate
    esc_payload = {"escalation_reason": "Urgent technical issue"}
    response = client.post(f"/enquiry/{enquiry_id}/escalate", json=esc_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["updated_status"] == "escalated"
    assert data["escalation_reason"] == "Urgent technical issue"

    # 3. Verify DB state
    from app.db.models.enquiry import Enquiry

    enquiry = db_session.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    assert enquiry.status == EnquiryStatus.ESCALATED
    assert enquiry.priority == PriorityLevel.HIGH


def test_escalate_enquiry_idempotency(client, db_session):
    # Create and escalate
    enq_resp = client.post(
        "/enquiry/",
        json={
            "customer_name": "Idem User",
            "channel": "email",
            "message": "Can you share your pricing plans?",
        },
    )
    enquiry_id = enq_resp.json()["enquiry_id"]

    esc_payload = {"escalation_reason": "First time"}
    client.post(f"/enquiry/{enquiry_id}/escalate", json=esc_payload)

    # Escalate again
    response = client.post(f"/enquiry/{enquiry_id}/escalate", json=esc_payload)
    assert response.status_code == 200  # Still 200

    # Verify only one escalation history event with specific message
    from app.db.models.history_event import HistoryEvent
    from app.core.enums import EventType

    esc_events = (
        db_session.query(HistoryEvent)
        .filter(
            HistoryEvent.enquiry_id == enquiry_id,
            HistoryEvent.event_type == EventType.ESCALATED,
            HistoryEvent.message == "Enquiry manually escalated for management review.",
        )
        .all()
    )
    assert len(esc_events) == 1
