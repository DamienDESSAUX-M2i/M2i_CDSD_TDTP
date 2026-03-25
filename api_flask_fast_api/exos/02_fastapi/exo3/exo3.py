import re
from enum import StrEnum

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field, field_validator


class Category(StrEnum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"
    OTHER = "Other"


class SupplierCreate(BaseModel):
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


class Supplier(SupplierCreate):
    id: int


class ProductCreate(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    category: Category
    stock: int = Field(..., ge=0)
    supplier_id: int


class Product(ProductCreate):
    id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Category
    stock: int
    supplier: Supplier


suppliers_db: dict[int, dict] = {}
products_db: dict[int, dict] = {}

next_supplier_id = 1
next_product_id = 1

router_suppliers = APIRouter(prefix="/suppliers", tags=["suppliers"])
router_products = APIRouter(prefix="/products", tags=["products"])

# ===
#  Suppliers
# ===


@router_suppliers.get("/", response_model=list[Supplier])
def get_all_suppliers():
    return list(suppliers_db.values())


@router_suppliers.post("/", response_model=Supplier, status_code=201)
def create_supplier(supplier: SupplierCreate):
    global next_supplier_id

    new_supplier = {
        "id": next_supplier_id,
        "name": supplier.name,
        "email": supplier.email,
        "phone": supplier.phone,
    }

    suppliers_db[next_supplier_id] = new_supplier
    next_supplier_id += 1

    return new_supplier


# ===
# Products
# ===


@router_products.get("/", response_model=list[ProductResponse])
def get_all_products():
    result = []

    for product in products_db.values():
        supplier = suppliers_db.get(product["supplier_id"])

        if supplier:
            product["supplier"] = supplier

    return result


@router_products.post("/", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    global next_product_id

    if product.supplier_id not in suppliers_db:
        raise ValueError("Supplier not found")

    new_product = {
        "id": next_product_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "supplier_id": product.supplier_id,
    }

    products_db[next_product_id] = new_product
    next_product_id += 1

    return new_product
