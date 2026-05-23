from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils.time import get_utcnow

if TYPE_CHECKING:
    from .enquiry import Enquiry


class Followup(Base):
    __tablename__ = "followup"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enquiry_id: Mapped[int] = mapped_column(
        ForeignKey("enquiry.id", ondelete="CASCADE"), index=True
    )

    scheduled_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    template_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_utcnow
    )

    # Relationships
    enquiry: Mapped["Enquiry"] = relationship(back_populates="followups")
