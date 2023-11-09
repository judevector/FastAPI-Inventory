import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from dotenv import load_dotenv
import requests


from controllers import order_controller
from models.orders_model import Order

load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables and check for existence
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

if not redis_host or not redis_port:
    raise EnvironmentError("Redis environment variables are not set")

while True:
    # Establish Redis connection
    try:
        redis = get_redis_connection(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
        )
        print("Database connection established!")
        break
    except Exception as e:
        # Log the exception
        print(f"Failed to connect to Redis: {e}")
        time.sleep(2)


# # Initialize model with Redis connection
Order.Meta.database = redis


# Home Page Route
@app.get("/")
async def home():
    return {"message": "This is the Payment API Home Page"}


# Include routes
app.include_router(order_controller.router, prefix="/orders", tags=["orders"])
