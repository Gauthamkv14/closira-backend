from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models.enquiry import Enquiry
from app.db.models.followup import Followup
from app.schemas.followup import FollowupCreate
from app.services.history_service import HistoryService
from app.core.enums import EventType
from app.core.logging import logger
from app.utils.time import get_utcnow


class FollowupService:
    """
    Service layer for managing post-enquiry follow-up interactions.
    """

    @staticmethod
    def schedule_followup(
        db: Session, enquiry_id: int, followup_in: FollowupCreate
    ) -> Followup:
        """
        Schedules a new follow-up for a specific enquiry.
        """
        logger.info(
            "Scheduling follow-up",
            extra={"enquiry_id": enquiry_id, "delay": followup_in.delay_minutes},
        )

        # 1. Validate enquiry existence
        enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
        if not enquiry:
            logger.warning(
                "Follow-up failed: Enquiry not found", extra={"enquiry_id": enquiry_id}
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Enquiry with ID {enquiry_id} not found",
            )

        # 2. Calculate scheduled time
        scheduled_time = get_utcnow() + timedelta(minutes=followup_in.delay_minutes)

        # 3. Create Followup record
        db_followup = Followup(
            enquiry_id=enquiry_id,
            scheduled_time=scheduled_time,
            template_message=followup_in.template_message,
            completed=False,
        )
        db.add(db_followup)

        # Flush to get the followup ID
        db.flush()

        # 4. Record history event via HistoryService
        HistoryService.create_history_event(
            db=db,
            enquiry_id=enquiry_id,
            event_type=EventType.FOLLOWUP_SCHEDULED,
            message=f"Follow-up scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} UTC",
            metadata_json={
                "followup_id": db_followup.id,
                "delay_minutes": followup_in.delay_minutes,
                "scheduled_time": scheduled_time.isoformat(),
            },
        )

        try:
            db.commit()
            db.refresh(db_followup)
            logger.info(
                "Follow-up successfully scheduled",
                extra={"followup_id": db_followup.id},
            )
            return db_followup
        except Exception as e:
            db.rollback()
            logger.error("Failed to schedule follow-up", extra={"error": str(e)})
            raise
