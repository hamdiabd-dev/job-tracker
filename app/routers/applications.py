from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.application import (
    create_application,
    delete_application,
    get_application,
    list_applications,
    update_application,
)
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.application import ApplicationStatus
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationPublic,
    ApplicationUpdate,
)


router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationPublic])
async def list_my_applications(
    status_filter: ApplicationStatus | None = Query(default=None, alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    """List all applications belonging to the current user."""
    return await list_applications(
        db, user_id=current_user.id, status=status_filter, skip=skip, limit=limit
    )


@router.post("", response_model=ApplicationPublic, status_code=status.HTTP_201_CREATED)
async def create_my_application(
    application_in: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new application for the current user."""
    return await create_application(db, user_id=current_user.id, application_in=application_in)


@router.get("/{application_id}", response_model=ApplicationPublic)
async def get_my_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single application by ID — only if it belongs to the current user."""
    application = await get_application(db, application_id=application_id, user_id=current_user.id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.patch("/{application_id}", response_model=ApplicationPublic)
async def update_my_application(
    application_id: UUID,
    application_in: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an application — only if it belongs to the current user."""
    application = await get_application(db, application_id=application_id, user_id=current_user.id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return await update_application(db, application=application, application_in=application_in)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an application — only if it belongs to the current user."""
    application = await get_application(db, application_id=application_id, user_id=current_user.id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    await delete_application(db, application=application)