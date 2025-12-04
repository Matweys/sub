# auth/router.py
from fastapi import APIRouter, Body, HTTPException
from .schemas import Login
from .utils import create_access_token, USERS

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(user: Login = Body(...)):
    for key, value in USERS.items():
        if user.username == key and user.password == value['password']:
            data = {"sub": user.username, "role": value['role']}
            token = create_access_token(data)
            return {'access_token': token,
                    "token_type": "bearer"}

    raise HTTPException(status_code=403, detail="Forbidden")



