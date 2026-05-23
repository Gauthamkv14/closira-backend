import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.dependencies import get_db

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_test_sessions(monkeypatch):
    """
    Automatically monkeypatch the application's SessionLocal to use
    the testing session factory. This ensures background tasks and services
    use the in-memory test database.
    """
    from app.db import session as db_session_module
    from app.workers import enquiry_processor

    monkeypatch.setattr(db_session_module, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(enquiry_processor, "SessionLocal", TestingSessionLocal)


@pytest.fixture(scope="function")
def db_session():
    """Returns a fresh SQLAlchemy session for a test function."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Returns a TestClient with the dependency injected database."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
