from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.application import ApplicationStatus, WorkMode


class ApplicationBase(BaseModel):
    """Common fields shared across create/update/read."""

    company_name: str = Field(min_length=1, max_length=255)
    role_title: str = Field(min_length=1, max_length=255)
    job_url: HttpUrl | None = None
    recruiter_name: str | None = Field(default=None, max_length=255)
    recruiter_email: str | None = Field(default=None, max_length=255)
    proposed_ral_min: int | None = Field(default=None, ge=0, le=10_000_000)
    proposed_ral_max: int | None = Field(default=None, ge=0, le=10_000_000)
    location: str | None = Field(default=None, max_length=255)
    work_mode: WorkMode | None = None
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""

    current_status: ApplicationStatus = ApplicationStatus.SENT


class ApplicationUpdate(BaseModel):
    """Schema for updating an application — all fields optional."""

    company_name: str | None = Field(default=None, min_length=1, max_length=255)
    role_title: str | None = Field(default=None, min_length=1, max_length=255)
    job_url: HttpUrl | None = None
    recruiter_name: str | None = Field(default=None, max_length=255)
    recruiter_email: str | None = Field(default=None, max_length=255)
    proposed_ral_min: int | None = Field(default=None, ge=0, le=10_000_000)
    proposed_ral_max: int | None = Field(default=None, ge=0, le=10_000_000)
    location: str | None = Field(default=None, max_length=255)
    work_mode: WorkMode | None = None
    source: str | None = Field(default=None, max_length=100)
    current_status: ApplicationStatus | None = None
    notes: str | None = None


class ApplicationPublic(ApplicationBase):
    """Schema returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    current_status: ApplicationStatus
    created_at: datetime
    updated_at: datetime