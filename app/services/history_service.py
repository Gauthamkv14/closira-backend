from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.db.models.history_event import HistoryEvent
from app.core.enums import EventType
from app.core.logging import logger
from app.utils.time import get_utcnow


class HistoryService:
    """
    Centralized service for managing the enquiry audit trail and activity timeline.
    """

    @staticmethod
    def create_history_event(
        db: Session,
        enquiry_id: int,
        event_type: EventType,
        message: str,
        metadata_json: Optional[Dict[str, Any]] = None,
        commit: bool = False,
    ) -> HistoryEvent:
        """
        Creates and persists a history event for an enquiry.

        Args:
            db: SQLAlchemy session
            enquiry_id: The ID of the target enquiry
            event_type: The domain event type from core.enums
            message: Human-readable description of the event
            metadata_json: Optional dictionary containing event-specific data
            commit: If True, commits the transaction immediately. Defaults to False
                     to allow for atomic multi-model updates.
        """
        logger.info(
            "Recording history event",
            extra={
                "enquiry_id": enquiry_id,
                "event_type": event_type,
                "event_description": message,
            },
        )

        history_event = HistoryEvent(
            enquiry_id=enquiry_id,
            event_type=event_type,
            message=message,
            metadata_json=metadata_json,
            created_at=get_utcnow(),
        )

        db.add(history_event)

        if commit:
            try:
                db.commit()
                db.refresh(history_event)
            except Exception as e:
                db.rollback()
                logger.error("Failed to persist history event", extra={"error": str(e)})
                raise

        return history_event
