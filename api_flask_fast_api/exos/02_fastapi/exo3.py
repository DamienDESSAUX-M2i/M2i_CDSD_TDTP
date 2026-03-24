import re
from enum import StrEnum

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator


class Category(StrEnum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"
    OTHER = "Other"


class Supplier(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v

        if not re.match(r"^[\d\s\-\(\)]+$", v):
            raise ValueError("Invalid phone format")

        digits_only = re.sub(r"\D", "", v)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError("Phone must have 10-15 digits")

        return v


class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class Product(BaseModel):
    id: int
    name: str
    price: float = Field(..., gt=0)
    category: Category
    stock: int = Field(..., ge=0)
    supplier_id: int


class ProductCreate(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    category: Category
    stock: int = Field(..., ge=0)
    supplier_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Category
    stock: int
    supplier: Supplier


suppliers_db: dict[int, Supplier] = {}
products_db: dict[int, Product] = {}

next_supplier_id = 1
next_product_id = 1

app = FastAPI(title="Mon API", version="1.0.0")

# ===
#  Suppliers
# ===


@app.get("/suppliers", response_model=list[Supplier], tags=["suppliers"])
def get_all_suppliers():
    return list(suppliers_db.values())


@app.post("/suppliers", response_model=Supplier, status_code=201, tags=["suppliers"])
def create_supplier(supplier: SupplierCreate):
    global next_supplier_id

    new_supplier = Supplier(
        id=next_supplier_id,
        name=supplier.name,
        email=supplier.email,
        phone=supplier.phone,
    )

    suppliers_db[next_supplier_id] = new_supplier
    next_supplier_id += 1

    return new_supplier


# ===
# Products
# ===


@app.get("/products", response_model=list[ProductResponse], tags=["products"])
def get_all_products():
    result = []

    for product in products_db.values():
        supplier = suppliers_db.get(product.supplier_id)

        if supplier:
            result.append(
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    category=product.category,
                    stock=product.stock,
                    supplier=supplier,
                )
            )

    return result


@app.post("/products", response_model=Product, status_code=201, tags=["products"])
def create_product(product: ProductCreate):
    global next_product_id

    if product.supplier_id not in suppliers_db:
        raise ValueError("Supplier not found")

    new_product = Product(
        id=next_product_id,
        name=product.name,
        price=product.price,
        category=product.category,
        stock=product.stock,
        supplier_id=product.supplier_id,
    )

    products_db[next_product_id] = new_product
    next_product_id += 1

    return new_product


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
