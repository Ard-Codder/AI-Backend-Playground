"""
Authentication routes
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ..auth.security import create_access_token
from ..config import settings
from ..db import get_db
from ..schemas.auth import Token
from ..schemas.user import UserCreate, UserResponse
from ..services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse)  # type: ignore
async def register(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Register a new user"""
    user_service = UserService(db)

    # Check if user already exists
    existing_user = await user_service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    existing_user = await user_service.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    try:
        user = await user_service.create_user(user_data)
        return UserResponse.model_validate(user)  # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)  # type: ignore
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    """User login"""
    user_service = UserService(db)

    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
