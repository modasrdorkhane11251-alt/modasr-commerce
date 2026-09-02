"""Wallet and ledger schemas."""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional


class WalletResponse(BaseModel):
    """Wallet response schema."""
    id: int
    user_id: int
    balance: Decimal
    hold_amount: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @property
    def available_balance(self) -> Decimal:
        """Calculate available balance."""
        return self.balance - self.hold_amount


class WalletTransactionResponse(BaseModel):
    """Wallet transaction response schema."""
    id: int
    wallet_id: int
    type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DepositRequest(BaseModel):
    """Deposit request schema."""
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None
