"""Wallet endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.wallet import WalletResponse, WalletTransactionResponse, DepositRequest

router = APIRouter()


@router.get("/", response_model=WalletResponse)
async def get_wallet(db: AsyncSession = Depends(get_db)):
    """
    Get current user's wallet.
    """
    # TODO: Implement get wallet
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/transactions", response_model=List[WalletTransactionResponse])
async def list_transactions(db: AsyncSession = Depends(get_db)):
    """
    List wallet transactions.
    """
    # TODO: Implement list transactions
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/deposit", response_model=WalletResponse)
async def deposit(deposit_request: DepositRequest, db: AsyncSession = Depends(get_db)):
    """
    Deposit funds to wallet.
    """
    # TODO: Implement deposit
    raise HTTPException(status_code=501, detail="Not implemented")
