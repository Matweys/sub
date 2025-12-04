# products/router.py
from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_check_users
from typing import Dict
from .schemas import CreateProducts
from .models import Product
from database import get_db

router = APIRouter(prefix="/products", tags=["Products"])



@router.get("/my")
async def my(
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Product).where(Product.owner == user["sub"])
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/create")
async def create(
    items: CreateProducts,
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db),
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    new_item = Product(
        name=items.name,
        price=items.price,
        category=items.category,
        owner=items.owner,
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return {"status": "success", "product": new_item}


@router.get("/all")
async def all_products(
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db),
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    stmt = select(Product)
    result = await db.execute(stmt)
    return result.scalars().all()

