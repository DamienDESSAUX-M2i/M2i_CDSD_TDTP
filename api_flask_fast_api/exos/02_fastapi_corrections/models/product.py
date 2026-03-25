from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    OTHER = "other"


class Supplier(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Nom du fournisseur")
    email: EmailStr = Field(..., description="Email du fournisseur")
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\-\s()]{10,}$", description="Téléphone")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Acme Supplier",
                "email": "contact@acme.com",
                "phone": "+33123456789"
            }
        }
    )


class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Nom du produit")
    price: float = Field(..., gt=0, description="Prix > 0")
    category: ProductCategory = Field(..., description="Catégorie du produit")
    stock: int = Field(..., ge=0, description="Stock ≥ 0")
    supplier: Supplier = Field(..., description="Informations du fournisseur")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "category": "electronics",
                "stock": 50,
                "supplier": {
                    "name": "Tech Supplier",
                    "email": "contact@techsupplier.com",
                    "phone": "+33123456789"
                }
            }
        }
    )

    @field_validator("price")
    @classmethod
    def validate_price_reasonable(cls, v: float) -> float:
        if v > 1_000_000:
            raise ValueError("Price seems unreasonably high")
        return v