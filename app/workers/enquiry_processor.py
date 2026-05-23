from app.db.session import SessionLocal
from app.db.models.enquiry import Enquiry
from app.db.models.history_event import HistoryEvent
from app.services.sop_matcher import SOPMatcherService
from app.core.enums import EnquiryStatus, EventType
from app.core.logging import logger


def process_enquiry_task(enquiry_id: int):
    """
    Background worker task to process a new enquiry.

    This function:
    1. Runs the SOP matcher
    2. Updates the enquiry record with the match results
    3. Records the event in the history timeline
    4. Handles escalations if no match is found
    """
    db = SessionLocal()
    try:
        logger.info("Starting background processing", extra={"enquiry_id": enquiry_id})

        enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
        if not enquiry:
            logger.error(
                "Enquiry not found in background task", extra={"enquiry_id": enquiry_id}
            )
            return

        # 1. Run the SOP Matcher logic
        match_result = SOPMatcherService.match_enquiry(enquiry.message)

        # 2. Map match results to the enquiry model
        enquiry.matched_sop = match_result.matched_sop
        enquiry.suggested_response = match_result.suggested_response

        # 3. Determine new status
        new_status = (
            EnquiryStatus.ESCALATED
            if match_result.escalation_required
            else EnquiryStatus.PROCESSED
        )
        enquiry.status = new_status

        # 4. Create history event for audit trail
        event_message = (
            f"SOP Matched: {match_result.matched_sop}"
            if not match_result.escalation_required
            else "Enquiry escalated: No automated match found or critical category detected."
        )

        history_event = HistoryEvent(
            enquiry_id=enquiry.id,
            event_type=(
                EventType.ESCALATED
                if match_result.escalation_required
                else EventType.SOP_MATCHED
            ),
            message=event_message,
            metadata_json=match_result.to_dict(),
        )
        db.add(history_event)

        db.commit()
        logger.info(
            "Background processing completed",
            extra={
                "enquiry_id": enquiry_id,
                "status": new_status,
                "sop": match_result.matched_sop,
            },
        )

    except Exception as e:
        logger.error(
            "Error in background processing",
            extra={"enquiry_id": enquiry_id, "error": str(e)},
        )
        db.rollback()
    finally:
        db.close()
