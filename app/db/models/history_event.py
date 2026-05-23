from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict
from datetime import datetime
from sqlalchemy import Text, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import EventType
from app.utils.time import get_utcnow

if TYPE_CHECKING:
    from .enquiry import Enquiry


class HistoryEvent(Base):
    __tablename__ = "history_event"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enquiry_id: Mapped[int] = mapped_column(
        ForeignKey("enquiry.id", ondelete="CASCADE"), index=True
    )

    event_type: Mapped[EventType] = mapped_column(Enum(EventType), index=True)
    message: Mapped[str] = mapped_column(Text)

    # metadata_json allows us to store extra context about the event (e.g. status changes, SOP details)
    metadata_json: Mapped[Dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_utcnow, index=True
    )

    # Relationships
    enquiry: Mapped["Enquiry"] = relationship(back_populates="history_events")
