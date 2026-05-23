from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models.enquiry import Enquiry
from app.schemas.escalation import EscalationCreate, EscalationResponse
from app.services.history_service import HistoryService
from app.core.enums import EnquiryStatus, PriorityLevel, EventType
from app.core.logging import logger
from app.utils.time import get_utcnow


class EscalationService:
    """
    Service layer for managing enquiry escalations and priority shifts.
    """

    @staticmethod
    def escalate_enquiry(
        db: Session, enquiry_id: int, escalation_in: EscalationCreate
    ) -> EscalationResponse:
        """
        Escalates an enquiry, updates its priority, and records the event.
        Is idempotent - if already escalated, it returns the current state without duplicate events.
        """
        logger.info("Escalating enquiry", extra={"enquiry_id": enquiry_id})

        # 1. Fetch enquiry
        enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
        if not enquiry:
            logger.warning(
                "Escalation failed: Enquiry not found", extra={"enquiry_id": enquiry_id}
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Enquiry with ID {enquiry_id} not found",
            )

        # 2. Check for existing escalation (idempotency)
        if enquiry.status == EnquiryStatus.ESCALATED:
            logger.info(
                "Enquiry already escalated, returning current state",
                extra={"enquiry_id": enquiry_id},
            )
            # Find the history event for the escalation time or just use now/updated_at
            # For simplicity, we just return the current enquiry details
            return EscalationResponse(
                enquiry_id=enquiry.id,
                updated_status=enquiry.status,
                escalation_reason=escalation_in.escalation_reason,  # Or fetch from history if needed
                escalated_at=enquiry.updated_at or get_utcnow(),
            )

        # 3. Perform escalation updates
        enquiry.status = EnquiryStatus.ESCALATED
        enquiry.priority = PriorityLevel.HIGH

        # 4. Record history event
        HistoryService.create_history_event(
            db=db,
            enquiry_id=enquiry_id,
            event_type=EventType.ESCALATED,
            message="Enquiry manually escalated for management review.",
            metadata_json={
                "reason": escalation_in.escalation_reason,
                "previous_status": EnquiryStatus.PROCESSED,  # Assumption
                "priority_shift": "HIGH",
            },
        )

        try:
            db.commit()
            db.refresh(enquiry)
            logger.info(
                "Enquiry successfully escalated", extra={"enquiry_id": enquiry_id}
            )

            return EscalationResponse(
                enquiry_id=enquiry.id,
                updated_status=enquiry.status,
                escalation_reason=escalation_in.escalation_reason,
                escalated_at=get_utcnow(),
            )
        except Exception as e:
            db.rollback()
            logger.error("Failed to escalate enquiry", extra={"error": str(e)})
            raise
