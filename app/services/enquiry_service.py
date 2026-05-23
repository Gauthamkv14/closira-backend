from sqlalchemy.orm import Session
from app.db.models.enquiry import Enquiry
from app.db.models.history_event import HistoryEvent
from app.schemas.enquiry import EnquiryCreate
from app.core.enums import EnquiryStatus, EventType
from app.core.logging import logger


class EnquiryService:
    """
    Service Layer responsible for business logic related to customer enquiries.
    """

    @staticmethod
    def create_enquiry(db: Session, enquiry_in: EnquiryCreate) -> Enquiry:
        """
        Creates a new customer enquiry record and initializes its history timeline.
        """
        logger.info(
            "Creating new enquiry",
            extra={
                "customer_name": enquiry_in.customer_name,
                "channel": enquiry_in.channel,
            },
        )

        # 1. Initialize the Enquiry record
        db_enquiry = Enquiry(
            customer_name=enquiry_in.customer_name,
            channel=enquiry_in.channel,
            message=enquiry_in.message,
            status=EnquiryStatus.RECEIVED,
        )
        db.add(db_enquiry)

        # Flush to get the ID without committing the full transaction yet
        db.flush()

        # 2. Record the initial history event
        history_event = HistoryEvent(
            enquiry_id=db_enquiry.id,
            event_type=EventType.CREATED,
            message="Enquiry received and queued for processing.",
            metadata_json={
                "initial_status": EnquiryStatus.RECEIVED,
                "channel": enquiry_in.channel,
            },
        )
        db.add(history_event)

        try:
            db.commit()
            db.refresh(db_enquiry)
            logger.info(
                "Enquiry successfully persisted", extra={"enquiry_id": db_enquiry.id}
            )
            return db_enquiry

        except Exception as e:
            db.rollback()
            logger.error("Failed to create enquiry", extra={"error": str(e)})
            raise
