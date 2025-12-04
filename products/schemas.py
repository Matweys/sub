# products/schemas.py
from pydantic import BaseModel, Field


class CreateProducts(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)
    category: str
    owner: str
