from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.schemas.enquiry import EnquiryCreate
from app.schemas.enquiry_acknowledgement import EnquiryAcknowledgement
from app.schemas.followup import FollowupCreate, FollowupResponse
from app.schemas.escalation import EscalationCreate, EscalationResponse
from app.schemas.history import EnquiryHistoryResponse
from app.api.dependencies import get_db
from app.db.models.enquiry import Enquiry
from app.services.enquiry_service import EnquiryService
from app.services.followup_service import FollowupService
from app.services.escalation_service import EscalationService
from app.workers.enquiry_processor import process_enquiry_task
from app.core.logging import logger

router = APIRouter()


@router.post(
    "/",
    response_model=EnquiryAcknowledgement,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Customer Enquiry",
    description="""
Accepts a new customer enquiry for processing.

**Workflow:**
1. **Validation**: Immediate validation of message length and channel.
2. **Persistence**: Enquiry is saved with 'received' status.
3. **Acknowledgement**: API returns a 201 Created with a tracking ID.
4. **Async Processing**: A background task triggers SOP matching and suggested response generation.
    """,
    responses={
        201: {
            "description": "Enquiry accepted and queued for processing",
            "content": {
                "application/json": {
                    "example": {
                        "enquiry_id": 123,
                        "status": "received",
                        "processing_state": "queued",
                        "created_at": "2026-05-23T16:17:42Z",
                    }
                }
            },
        }
    },
)
def create_enquiry(
    enquiry_in: EnquiryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Ingest a customer enquiry and initiate asynchronous processing.
    """
    # 1. Synchronous persistence
    enquiry = EnquiryService.create_enquiry(db, enquiry_in)

    # 2. Trigger asynchronous background task
    background_tasks.add_task(process_enquiry_task, enquiry.id)

    logger.info(
        "Enquiry ingestion successful",
        extra={"enquiry_id": enquiry.id, "status": enquiry.status},
    )

    # Return acknowledgement-style response
    return {
        "enquiry_id": enquiry.id,
        "status": enquiry.status,
        "processing_state": "queued",
        "created_at": enquiry.created_at,
    }


@router.post(
    "/{enquiry_id}/follow-up",
    response_model=FollowupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule Follow-up",
    description="""
Schedule an automated follow-up message for a specific enquiry.

This ensures the customer receives a response if no action is taken manually.
Records the scheduling event in the enquiry timeline.
    """,
    responses={
        201: {"description": "Follow-up scheduled successfully"},
        404: {"description": "Enquiry not found"},
        422: {"description": "Validation error (e.g. invalid delay)"},
    },
)
def schedule_enquiry_followup(
    enquiry_id: int, followup_in: FollowupCreate, db: Session = Depends(get_db)
):
    """
    Schedule a follow-up for the given enquiry ID.
    """
    return FollowupService.schedule_followup(db, enquiry_id, followup_in)


@router.post(
    "/{enquiry_id}/escalate",
    response_model=EscalationResponse,
    status_code=status.HTTP_200_OK,
    summary="Escalate Enquiry",
    description="""
Manually escalate an enquiry to High Priority.

Updates status to 'escalated', sets priority to 'high', and records
the event in the activity timeline. Idempotent: multiple calls to 
escalate the same enquiry will not create duplicate events.
    """,
    responses={
        200: {"description": "Enquiry escalated successfully"},
        404: {"description": "Enquiry not found"},
    },
)
def escalate_enquiry_route(
    enquiry_id: int, escalation_in: EscalationCreate, db: Session = Depends(get_db)
):
    """
    Escalate the given enquiry ID.
    """
    return EscalationService.escalate_enquiry(db, enquiry_id, escalation_in)


@router.get(
    "/{enquiry_id}/history",
    response_model=EnquiryHistoryResponse,
    summary="Get Enquiry Timeline",
    description="""
Retrieve a complete chronological history of all activities related 
to a specific customer enquiry.

Includes creation, SOP matching, suggested responses, follow-up cycles,
and escalations in a CRM-style timeline.
    """,
    responses={
        200: {"description": "Timeline retrieved successfully"},
        404: {"description": "Enquiry not found"},
    },
)
def get_enquiry_timeline_route(enquiry_id: int, db: Session = Depends(get_db)):
    """
    Fetch the activity timeline for the given enquiry ID.
    """
    return EnquiryService.get_enquiry_history(db, enquiry_id)
