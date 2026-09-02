"""Order schemas."""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional, List


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    quantity: int = Field(default=1, ge=1)


class OrderItemResponse(OrderItemBase):
    """Order item response schema."""
    id: int
    order_id: int
    product_name: str
    unit_price: Decimal
    subtotal: Decimal
    fulfillment_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Order creation schema."""
    items: List[OrderItemBase] = Field(..., min_items=1)
    coupon_code: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_notes: Optional[str] = None


class OrderUpdate(BaseModel):
    """Order update schema."""
    status: Optional[str] = None
    internal_notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Order response schema."""
    id: int
    order_number: str
    user_id: int
    status: str
    fulfillment_status: str
    subtotal: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime]

    class Config:
        from_attributes = True
