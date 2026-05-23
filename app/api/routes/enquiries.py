from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.enquiry import EnquiryCreate
from app.schemas.enquiry_acknowledgement import EnquiryAcknowledgement
from app.services.enquiry_service import EnquiryService
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
