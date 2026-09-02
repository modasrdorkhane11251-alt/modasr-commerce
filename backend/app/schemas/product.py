"""Product schemas."""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict, Any


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Category creation schema."""
    pass


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: int
    tenant_id: int
    slug: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=255)
    category_id: int
    description: Optional[str] = None
    type: str  # DIGITAL_PRODUCT, SERVICE, SUBSCRIPTION, etc.
    base_price: Decimal = Field(..., gt=0)


class ProductCreate(ProductBase):
    """Product creation schema."""
    quantity_total: Optional[int] = None
    is_unlimited: bool = False


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Product response schema."""
    id: int
    tenant_id: int
    slug: str
    quantity_sold: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
