"""User endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(db: AsyncSession = Depends(get_db)):
    """
    Get current authenticated user profile.
    """
    # TODO: Implement get current user
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/me", response_model=UserResponse)
async def update_current_user(user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update current user profile.
    """
    # TODO: Implement update user
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by ID.
    """
    # TODO: Implement get user
    raise HTTPException(status_code=501, detail="Not implemented")
