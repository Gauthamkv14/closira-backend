from __future__ import annotations
from typing import TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import ChannelType, EnquiryStatus, PriorityLevel
from app.utils.time import get_utcnow

if TYPE_CHECKING:
    from .followup import Followup
    from .history_event import HistoryEvent


class Enquiry(Base):
    __tablename__ = "enquiry"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[ChannelType] = mapped_column(Enum(ChannelType), index=True)
    message: Mapped[str] = mapped_column(Text)

    status: Mapped[EnquiryStatus] = mapped_column(
        Enum(EnquiryStatus), default=EnquiryStatus.RECEIVED, index=True
    )
    priority: Mapped[PriorityLevel] = mapped_column(
        Enum(PriorityLevel), default=PriorityLevel.MEDIUM
    )

    # These fields are populated by the background SOP worker
    matched_sop: Mapped[str | None] = mapped_column(String(255), nullable=True)
    suggested_response: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_utcnow, onupdate=get_utcnow
    )

    # Relationships
    # Using 'cascade="all, delete-orphan"' ensures that when an enquiry is deleted,
    # its followups and history are also cleaned up.
    followups: Mapped[List["Followup"]] = relationship(
        back_populates="enquiry", cascade="all, delete-orphan"
    )
    history_events: Mapped[List["HistoryEvent"]] = relationship(
        back_populates="enquiry", cascade="all, delete-orphan"
    )
