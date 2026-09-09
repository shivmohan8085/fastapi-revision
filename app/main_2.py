from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Product(BaseModel):
    id      : int
    name    : str
    price   : float
    stock   : int|None = None


@app.post('/products')
async def create_product(new_product:Product):
    product_dict = new_product.model_dump()
    product_with_tax = new_product.price + (new_product.price * 18 / 100)
    product_dict.update({"product_with_tax": product_with_tax})
    # return new_product
    return product_dict