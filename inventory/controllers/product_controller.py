from models.product_model import Product
from fastapi import APIRouter, HTTPException, status
from redis_om.model.model import NotFoundError
from starlette.requests import Request

router = APIRouter()


# Get all product IDs
@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
def get_all_products():
    try:
        return [format(pk) for pk in Product.all_pks()]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function used for getting all products in a list
def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


# Create a new product
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_all_products(request: Request):
    body = await request.json()
    try:
        product = Product(
            name=body["name"],
            price=body["price"],
            quantity=body["quantity"],
        )
        product.save()
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)} is missing")


# Get individual product using primary key
@router.get("/{pk}", status_code=status.HTTP_200_OK)
def get_product(pk: str):
    try:
        product = Product.get(pk)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with pk {pk} does not exist.",
            )
        return Product.get(pk)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with pk {pk} does not exist.",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete an individual product using primary key
@router.delete("/{pk}", status_code=status.HTTP_200_OK)
def delete_product(pk: str):
    try:
        product = Product.get(pk)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with pk {pk} does not exist.",
            )
        Product.delete(pk)
        return {"status": "OK"}
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with pk {pk} does not exist.",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
