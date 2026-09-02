"""Payment schemas."""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, Any


class PaymentMethodResponse(BaseModel):
    """Payment method response schema."""
    id: int
    tenant_id: int
    name: str
    provider: str
    code: str
    is_active: bool
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    """Payment creation schema."""
    order_id: int
    payment_method_id: int


class PaymentResponse(BaseModel):
    """Payment response schema."""
    id: int
    order_id: int
    transaction_id: Optional[str]
    amount: Decimal
    fee_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]
    paid_at: Optional[datetime]

    class Config:
        from_attributes = True


class PaymentVerifyRequest(BaseModel):
    """Payment verification request."""
    payment_id: int
    gateway_data: Dict[str, Any] = {}


class PaymentCallbackRequest(BaseModel):
    """Generic payment callback request."""
    status: str
    transaction_id: Optional[str] = None
    order_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}
