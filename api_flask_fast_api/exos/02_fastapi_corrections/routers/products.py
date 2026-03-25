from fastapi import APIRouter, HTTPException, status

from models.product import Product
from db import product_db


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):

    product_dict = product.model_dump()
    product_dict["id"] = product_db.next_product_id
    product_db.products_db[product_db.next_product_id] = product_dict
    product_db.next_product_id += 1


    return product_dict


@router.get("/{product_id}")
async def get_product(product_id: int):
    if product_id not in product_db.products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product_db.products_db[product_id]