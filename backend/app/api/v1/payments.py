"""Payment endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.payment import PaymentResponse, PaymentCreate, PaymentMethodResponse

router = APIRouter()


@router.get("/methods", response_model=List[PaymentMethodResponse])
async def list_payment_methods(db: AsyncSession = Depends(get_db)):
    """
    List available payment methods.
    """
    # TODO: Implement list payment methods
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("", response_model=PaymentResponse)
async def create_payment(payment_data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a payment for an order.
    """
    # TODO: Implement create payment
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get payment details.
    """
    # TODO: Implement get payment
    raise HTTPException(status_code=501, detail="Not implemented")
