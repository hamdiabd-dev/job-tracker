from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import get_user_by_id
from app.database import get_db
from app.models.user import User
from app.security import decode_access_token


# Tells FastAPI to look for tokens in the Authorization header (Bearer scheme)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract the JWT from the request, verify it, and return the current user.
    Raises 401 if the token is invalid, expired, or the user no longer exists.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_error

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise credentials_error

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_error

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_error

    return user