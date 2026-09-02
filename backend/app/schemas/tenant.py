"""Tenant schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class TenantBase(BaseModel):
    """Base tenant schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    website_url: Optional[str] = None


class TenantCreate(TenantBase):
    """Tenant creation schema."""
    telegram_bot_token: str = Field(..., min_length=10)


class TenantUpdate(BaseModel):
    """Tenant update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class TenantResponse(TenantBase):
    """Tenant response schema."""
    id: int
    slug: str
    telegram_bot_username: Optional[str]
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
