"""API v1 module."""
from fastapi import APIRouter
from app.api.v1 import auth, users, products, orders, wallet, payments

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])

__all__ = ["api_router"]
