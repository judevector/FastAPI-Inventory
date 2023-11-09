import asyncio
import httpx
from models.orders_model import Order
from fastapi import APIRouter, HTTPException, status
from fastapi.background import BackgroundTasks
from redis_om.model.model import NotFoundError
from starlette.requests import Request
import requests

router = APIRouter()


# Get Orders
@router.get("/{pk}", status_code=status.HTTP_200_OK)
def get_all_orders(pk: str):
    return Order.get(pk)


# Create an Order
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://localhost:8000/products/{body['id']}")
            product = resp.json()

        order = Order(
            product_id=body["id"],
            price=product["price"],
            fee=0.2 * product["price"],
            total=1.2 * product["price"],
            quantity=body["quantity"],
            status="pending",
        )
        order.save()

        background_tasks.add_task(order_completed, order)

        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def order_completed(order: Order):
    await asyncio.sleep(5)
    order.status = "completed"
    order.save()
