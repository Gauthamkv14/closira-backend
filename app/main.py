from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.logging import setup_logging
from app.core.exceptions import (
    ClosiraException,
    custom_exception_handler,
    validation_exception_handler,
)
from app.db.session import engine
from app.db.base import Base

# Import models to ensure they are registered for table creation

from app.api.routes import health, enquiries

# Set up logging globally
setup_logging()

tags_metadata = [
    {
        "name": "Health",
        "description": "Service availability and monitoring endpoints.",
    },
    {
        "name": "Enquiries",
        "description": "Intake and management of customer enquiries.",
    },
    {
        "name": "Follow-ups",
        "description": "Scheduling and tracking automated customer follow-ups.",
    },
    {
        "name": "Escalations",
        "description": "Logic for handling high-priority or complex enquiry redirections.",
    },
    {
        "name": "History",
        "description": "Timeline and audit trail for enquiry lifecycle events.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Closira API",
    version="1.0.0",
    description="""
Async enquiry-processing backend for Closira's AI-powered customer communication workflows.

### Key Features:
* **Enquiry Intake**: Accept messages from multiple channels (Chat, Email, Social).
* **SOP Matching**: Automated analysis using keyword-based logic (simulating AI).
* **Escalation Workflows**: High-priority routing for unhandled cases.
* **Follow-up Scheduling**: Delayed customer retention messaging.
* **History Tracking**: Robust audit trail of all status changes and interactions.
    """,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

# Exception handlers
app.add_exception_handler(ClosiraException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(enquiries.router, prefix="/enquiry", tags=["Enquiries"])

# Other routers will be included here as they are developed
