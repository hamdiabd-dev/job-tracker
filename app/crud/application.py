from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate


async def get_application(
    db: AsyncSession, application_id: UUID, user_id: UUID
) -> Application | None:
    """
    Get one application by ID, but only if it belongs to the given user.
    Ownership is enforced here.
    """
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def list_applications(
    db: AsyncSession,
    user_id: UUID,
    status: ApplicationStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Application]:
    """List all applications for a user, optionally filtered by status."""
    query = select(Application).where(Application.user_id == user_id)
    if status is not None:
        query = query.where(Application.current_status == status)
    query = query.order_by(Application.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_application(
    db: AsyncSession, user_id: UUID, application_in: ApplicationCreate
) -> Application:
    """Create a new application owned by the given user."""
    data = application_in.model_dump(mode="json")
    application = Application(user_id=user_id, **data)
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


async def update_application(
    db: AsyncSession,
    application: Application,
    application_in: ApplicationUpdate,
) -> Application:
    """Apply partial updates to an existing application."""
    update_data = application_in.model_dump(mode="json", exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
    await db.commit()
    await db.refresh(application)
    return application


async def delete_application(db: AsyncSession, application: Application) -> None:
    """Delete an application."""
    await db.delete(application)
    await db.commit()