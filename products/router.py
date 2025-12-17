# products/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from auth.utils import get_check_users
from database.db import get_db
from products.schemas import CreateProducts
from products.services import create_product, get_all_products, get_products_by_owner

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/my")
async def my(
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db),
):
    return await get_products_by_owner(db, user["sub"])


@router.post("/create")
async def create(
    items: CreateProducts,
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db),
):
    new_item = await create_product(user, items, db)
    return {"status": "success", "product": new_item}


@router.get("/all")
async def all_products(
    user: Dict = Depends(get_check_users),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_products(user, db)
