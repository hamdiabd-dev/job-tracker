import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApplicationStatus(str, enum.Enum):
    """All possible states of a job application."""

    SENT = "sent"
    WAITING = "waiting"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    GHOSTED = "ghosted"
    WITHDRAWN = "withdrawn"


class WorkMode(str, enum.Enum):
    """Work location modes."""

    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Ownership
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Core info
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    # Recruiter
    recruiter_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recruiter_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Compensation
    proposed_ral_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proposed_ral_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Location
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_mode: Mapped[WorkMode | None] = mapped_column(
        Enum(WorkMode, name="work_mode_enum"), nullable=True
    )

    # Source (LinkedIn, agency, referral, etc.)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Current status
    current_status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status_enum"),
        nullable=False,
        default=ApplicationStatus.SENT,
    )

    # Free-form notes
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship back to user (optional but useful)
    user = relationship("User", backref="applications")