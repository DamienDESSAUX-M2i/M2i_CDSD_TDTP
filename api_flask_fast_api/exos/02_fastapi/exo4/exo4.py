from uuid import uuid4

from fastapi import APIRouter
from pydantic import UUID4, BaseModel, EmailStr, Field, model_validator


class Item(BaseModel):
    """Item Model"""

    item_id: int = Field(
        ...,
        title="Primary key",
        description="Item's ID",
        example=1,
    )
    quantity: int = Field(
        ...,
        ge=1,
        title="Quantity",
        description="Order's quantity",
        example=5,
    )
    price: float = Field(
        ...,
        ge=0,
        title="Price",
        description="Order's price",
        example=12.34,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "item_id": 1,
                "quantity": 5,
                "price": 12.34,
            }
        }
    }


class OrderCreate(BaseModel):
    """OrderCreation Model"""

    customer_email: EmailStr = Field(
        ...,
        title="Identifier",
        description="Order's identifier",
        example="user@example.com",
    )
    items: list[Item] = Field(
        ...,
        min_length=1,
        title="Identifier",
        description="Order's identifier",
        example=[
            {
                "item_id": 1,
                "quantity": 5,
                "price": 12.34,
            },
            {
                "item_id": 2,
                "quantity": 10,
                "price": 98.0,
            },
        ],
    )
    total: float | None = Field(
        None,
        title="Identifier",
        description="Order's identifier",
        example=1041.7,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_email": "user@example.com",
                "items": [
                    {
                        "item_id": 1,
                        "quantity": 5,
                        "price": 12.34,
                    },
                    {
                        "item_id": 2,
                        "quantity": 10,
                        "price": 98.0,
                    },
                ],
                "total": 1041.7,
            }
        }
    }

    @model_validator(mode="after")
    def validate_total(self):
        """Checks if total is correct according to the list of items"""
        total = sum(item.quantity * item.price for item in self.items)

        if self.total is None:
            self.total = total
            return self

        if self.total != total:
            raise ValueError("Given total doesn't match with compute total")

        return self


class Order(OrderCreate):
    """Order Model"""

    order_id: UUID4 = Field(
        ...,
        title="Primary key",
        description="Order's ID",
        example="3d0bdf4a-80ec-469e-8b8d-84e79d4fff72",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "order_id": "3d0bdf4a-80ec-469e-8b8d-84e79d4fff72",
                "customer_email": "user@example.com",
                "items": [
                    {
                        "item_id": 1,
                        "quantity": 5,
                        "price": 12.34,
                    },
                    {
                        "item_id": 2,
                        "quantity": 10,
                        "price": 98.0,
                    },
                ],
                "total": 1041.7,
            }
        }
    }


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=201)
def create_order(order: OrderCreate):
    """Create new order with automatic validation"""
    new_order = order.model_dump()
    new_order["order_id"] = uuid4()

    return new_order
