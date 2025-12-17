# core/exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from products.exceptions import (
    PermissionDenied,
    ProductCreateError,
    ProductGetAllError,
    ProductGetOwnerError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PermissionDenied)
    async def permission_denied_handler(request: Request, exc: PermissionDenied):
        return JSONResponse(
            status_code=403,
            content={"error": "PermissionDenied", "detail": str(exc)},
        )

    @app.exception_handler(ProductCreateError)
    async def product_create_error_handler(request: Request, exc: ProductCreateError):
        return JSONResponse(
            status_code=500,
            content={"error": "ProductCreateError", "detail": str(exc)},
        )

    @app.exception_handler(ProductGetAllError)
    async def product_get_all_error_handler(request: Request, exc: ProductGetAllError):
        return JSONResponse(
            status_code=500,
            content={"error": "ProductGetAllError", "detail": str(exc)},
        )

    @app.exception_handler(ProductGetOwnerError)
    async def product_get_owner_error_handler(request: Request, exc: ProductGetOwnerError):
        return JSONResponse(
            status_code=500,
            content={"error": "ProductGetOwnerError", "detail": str(exc)},
        )
