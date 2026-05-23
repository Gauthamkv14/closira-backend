from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# create_engine specific to sqlite
# check_same_thread=False is needed in FastAPI since multiple threads could interact with the same DB session
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False}
        if settings.DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
