from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator,model_validator


class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0, description="ID du produit")
    quantity: int = Field(..., ge=1, description="Quantité ≥ 1")
    price: float = Field(..., gt=0, description="Prix unitaire > 0")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": 1,
                "quantity": 2,
                "price": 99.99
            }
        }
    )


class Order(BaseModel):
    order_id: str = Field(..., description="ID unique de la commande")
    customer_email: EmailStr = Field(..., description="Email du client")
    items: List[OrderItem] = Field(..., min_length=1, description="Au moins 1 article")
    total: float = Field(..., gt=0, description="Total de la commande")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": "ORD-20240101-001",
                "customer_email": "customer@example.com",
                "items": [
                    {"product_id": 1, "quantity": 2, "price": 99.99},
                    {"product_id": 2, "quantity": 1, "price": 49.99}
                ],
                "total": 249.97
            }
        }
    )

    @field_validator("items")
    @classmethod
    def validate_items_not_empty(cls, v: List[OrderItem]) -> List[OrderItem]:
        if not v:
            raise ValueError("Order must have at least one item")
        return v

    @model_validator(mode="after")
    def validate_total_matches_items(self):
        calculated_total = sum(item.quantity * item.price for item in self.items)

        if abs(self.total - calculated_total) > 0.01:
            raise ValueError(
                f"Total must equal sum of items (expected {calculated_total:.2f}, got {self.total:.2f})"
            )

        return self