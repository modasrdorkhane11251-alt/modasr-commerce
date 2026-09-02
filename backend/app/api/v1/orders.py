"""Order endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.order import OrderResponse, OrderCreate

router = APIRouter()


@router.post("", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new order.
    """
    # TODO: Implement create order
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("", response_model=List[OrderResponse])
async def list_orders(db: AsyncSession = Depends(get_db)):
    """
    List user's orders.
    """
    # TODO: Implement list orders
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get order by ID.
    """
    # TODO: Implement get order
    raise HTTPException(status_code=501, detail="Not implemented")
