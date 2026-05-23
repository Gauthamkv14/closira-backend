from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.dependencies import get_db
from app.schemas.health import HealthResponse
from app.utils.time import get_utcnow

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verify the API operational status and database connectivity.",
    responses={
        200: {
            "description": "API and database are healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "database": "connected",
                        "timestamp": "2026-05-23T12:45:00Z",
                    }
                }
            },
        },
        503: {"description": "Service unhealthy"},
    },
)
def health_check(db: Session = Depends(get_db)):
    """
    Returns a 200 OK if both the API and database are functioning correctly.
    This is used by monitoring tools to ensure service availability.
    """
    is_db_ok = False
    try:
        # Proactively check DB connection
        db.execute(text("SELECT 1"))
        is_db_ok = True
    except Exception:
        # Any exception here indicates a connectivity issue
        pass

    return {
        "status": "healthy" if is_db_ok else "unhealthy",
        "database": "connected" if is_db_ok else "disconnected",
        "timestamp": get_utcnow(),
    }
