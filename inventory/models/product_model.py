from redis_om import HashModel
from pydantic import BaseModel


# Product Model for Database
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = None
