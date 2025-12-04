# main.py
from fastapi import FastAPI
import uvicorn
from auth.router import router as router_login
from products.router import router as router_products

app = FastAPI()

app.include_router(router_login)
app.include_router(router_products)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
