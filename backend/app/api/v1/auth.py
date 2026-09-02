"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import TokenRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserCreate, UserResponse
from app.security.jwt import create_access_token, create_refresh_token
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    
    - **user_data**: User registration data (username, email, password)
    """
    # TODO: Implement user registration
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/login", response_model=TokenResponse)
async def login(credentials: TokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Login user and get access token.
    
    - **credentials**: Email and password
    """
    # TODO: Implement login logic
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Refresh access token using refresh token.
    
    - **request**: Refresh token
    """
    # TODO: Implement token refresh logic
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/logout")
async def logout():
    """
    Logout user (revoke tokens).
    """
    # TODO: Implement logout logic
    return {"message": "Logged out successfully"}
