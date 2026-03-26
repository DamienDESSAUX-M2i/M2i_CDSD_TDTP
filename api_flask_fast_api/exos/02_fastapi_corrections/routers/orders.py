from fastapi import APIRouter, HTTPException, status
from models.order import Order
from db.memory import orders_db

router = APIRouter(tags=["Orders"])


@router.post("/orders", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    if order.order_id in orders_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order {order.order_id} already exists"
        )

    order_dict = order.model_dump()
    orders_db[order.order_id] = order_dict
    return order_dict


@router.get("/orders/{order_id}", response_model=dict)
async def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    return orders_db[order_id]