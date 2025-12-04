# main.py
from fastapi import FastAPI
import uvicorn
from auth.router import router as router_login
from products.router import router as router_products
from database import init_models

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_models()


app.include_router(router_login)
app.include_router(router_products)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
