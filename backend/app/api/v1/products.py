"""Product endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.product import ProductResponse, ProductCreate, CategoryResponse

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List product categories.
    """
    # TODO: Implement list categories
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("", response_model=List[ProductResponse])
async def list_products(
    category_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List products.
    
    - **category_id**: Filter by category (optional)
    - **skip**: Number of products to skip
    - **limit**: Maximum number of products to return
    """
    # TODO: Implement list products
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get product by ID.
    """
    # TODO: Implement get product
    raise HTTPException(status_code=501, detail="Not implemented")
