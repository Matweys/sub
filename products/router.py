# products/router.py
from fastapi import APIRouter, Body, HTTPException, Depends
from auth.utils import get_check_users
from typing import Dict
from .schemas import CreateProducts

router = APIRouter(prefix="/products", tags=["Products"])
PRODUCTS = [
    {"id": 1, "name": "iPhone", "price": 999, "category": "phones", "owner": "matwey"},
    {"id": 2, "name": "Samsung TV", "price": 1200, "category": "tv", "owner": "alex"},
    {"id": 3, "name": "MacBook", "price": 1999, "category": "laptops", "owner": "admin"}
]


@router.get("/my")
async def my(user: Dict = Depends(get_check_users)):
    result = []
    for product in PRODUCTS:
        if user['sub'] == product['owner']:
            result.append(product)

    return result


@router.post("/create")
async def create(items: CreateProducts = Body(...),
                 user: Dict = Depends(get_check_users)):
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="У вас нет доступа на добавление")

    next_id = max(product['id'] for product in PRODUCTS) + 1
    added_product = {"id": next_id, "name": items.name, "price": items.price,
                     "category": items.category, "owner": items.owner}
    result = {"status": "success", "product": added_product}
    return result


@router.get("/all")
async def products_all(user: Dict = Depends(get_check_users)):
    if user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    return PRODUCTS

