from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()

# submodel
class Category(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name", examples=["Electronics"])
    description: str | None = Field(default=None, max_length=500, description="Category description (optional)", examples=["Electronic items and gadgets"])

class Product(BaseModel):
    id: int = Field(..., gt=0, description="Unique product ID", examples=[1])  # ... means required
    name: str = Field(..., min_length=1, max_length=100, description="Product name", examples=["iPhone 15"])
    price: float = Field(..., gt=0, description="Product price", examples=[999.99])
    stock: int | None = Field(default=None, ge=0, description="Available stock (optional)", examples=[50])
    # category: Category | None = Field(default=None, description="Product category (optional)")  # single category
    category: list[Category] | None = Field(default=None, description="Product category (optional)", examples=[[{"name": "Electronics", "description": "Electronic items"}]])  # category list

class Seller(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Seller username", examples=["john_doe"])
    full_name: str | None = Field(default=None, max_length=100, description="Seller full name (optional)", examples=["John Doe"])

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
    
# With embed Truegit 
@app.post('/product-data')
def post_project_data(product:Annotated[Product, Body(embed=True)]):
    return {"product":product}




# submodel
class Category(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: str | None = Field(default=None, max_length=500, description="Category description (optional)")