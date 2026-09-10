from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()

class Product(BaseModel):
    id      : int
    name    : str
    price   : float
    stock   : int | None = None


class Seller(BaseModel):
    username: str
    full_name: str | None = None

@app.post('/products')
async def create_product(
    new_product:Product,
    seller:Seller|None,
    sec_key: Annotated[str, Body()]
    ):
    
    product_dict = new_product.model_dump()
    product_with_tax = new_product.price + (new_product.price * 18 / 100)
    product_dict.update({"product_with_tax": product_with_tax})
    # return new_product
    return {"product":product_dict , "seller":seller, "sec_key":sec_key}       


# add query parameter
@app.put('/products/{product_id}')
async def update_project(product_id:int, updated_project_dict:Product, discount: float|None = None):
    return { "product_id":product_id,
        "updated_project_dict":updated_project_dict,
        "discount":discount
         }
    
    
    
# With embed True
@app.post('/product-data')
def post_project_data(product:Annotated[Product, Body(embed=True)]):
    return {"product":product   }