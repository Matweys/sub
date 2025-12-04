# auth/utils.py
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Dict


oauth2_schema = OAuth2PasswordBearer(tokenUrl="Login")
secret_key = "test123"
algorithm = "HS256"
USERS = {
    "matwey": {"password": "adminpass", "role": "admin"},
    "alex": {"password": "123456", "role": "user"},
    "kate": {"password": "pass777", "role": "user"}
}


def create_access_token(data: Dict, expires_date: timedelta = None):
    to_encode = data.copy()
    exp_data = datetime.utcnow() + (expires_date if expires_date else timedelta(minutes=15))
    to_encode['exc'] = int(exp_data.timestamp())
    token = jwt.encode(to_encode, key=secret_key, algorithm=algorithm)
    return token


def get_check_users(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        if payload and payload['sub'] is None:
            raise HTTPException(status_code=403, detail="Forbidden")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload
