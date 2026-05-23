from app.core.enums import EnquiryStatus


def test_create_enquiry_api_success(client, db_session):
    payload = {
        "customer_name": "API Tester",
        "channel": "email",
        "message": "Hello, I want to book a meeting for next week.",
    }

    response = client.post("/enquiry/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "enquiry_id" in data
    assert data["status"] == "received"
    assert data["processing_state"] == "queued"
    assert "customer_name" not in data  # Response should be minimal acknowledgement

    # Verify the ID used in the response works for DB lookup
    enquiry_id = data["enquiry_id"]

    # Since TestClient runs background tasks before returning the response
    # (or shortly after in the same thread), we can check the DB state now.
    from app.db.models.enquiry import Enquiry

    db_enquiry = db_session.query(Enquiry).filter(Enquiry.id == enquiry_id).first()

    # The record in DB should have been updated by the background task
    assert db_enquiry.status == EnquiryStatus.PROCESSED
    assert db_enquiry.matched_sop == "Booking Request"


def test_create_enquiry_payload_validation(client):
    # Missing channel and name
    payload = {"message": "Too short"}
    response = client.post("/enquiry/", json=payload)
    assert response.status_code == 422
    assert "errors" in response.json()
