from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    FastAPI dependency that provides a SQLAlchemy session for a request.
    Closes the session once the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
