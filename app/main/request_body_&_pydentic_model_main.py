from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

app = FastAPI()

# =====================================================================
# Way 1: Field-Level Examples (Using `examples` inside Field)
# =====================================================================
# This approach defines examples on a per-field basis. 
# It is very useful when you want to document exactly what kind of data 
# goes into each specific property in the Swagger UI docs.

class CarCategory(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["SUV"])
    description: str | None = Field(default=None, max_length=500, examples=["Sport Utility Vehicle"])

class Car(BaseModel):
    id: int = Field(..., gt=0, examples=[1]) 
    name: str = Field(..., min_length=1, max_length=100, examples=["Toyota Fortuner"])
    price: float = Field(..., gt=0, examples=[45000.00])
    stock: int | None = Field(default=None, ge=0, examples=[10]) 
    category: list[CarCategory] | None = Field(default=None, examples=[[{"name": "SUV", "description": "Sport Utility Vehicle"}]])

class Dealer(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["toyota_central"])
    full_name: str | None = Field(default=None, max_length=100, examples=["Toyota Central Dealership"])


# =====================================================================
# Way 2: Model-Level Examples using a standard Dictionary (`model_config`)
# =====================================================================
# Instead of adding examples to every single field, this approach adds 
# a complete JSON example payload to the entire model using a dictionary.

class Topic(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Programming", "description": "Software development courses"}
            ]
        }
    }
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class Course(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 101,
                    "title": "Python Bootcamp",
                    "price": 49.99,
                    "stock": 100,
                    "category": [{"name": "Programming", "description": "Software development courses"}]
                }
            ]
        }
    }
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: int | None = Field(default=None, ge=0)
    category: list[Topic] | None = Field(default=None)

class Instructor(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"username": "john_dev", "full_name": "John Developer"}
            ]
        }
    }
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = Field(default=None, max_length=100)


# =====================================================================
# Way 3: Pydantic V2 `ConfigDict` (Recommended for Production)
# =====================================================================
# This is the most modern and robust way. `ConfigDict` gives you full 
# IDE support (type hints, autocomplete) and allows you to enforce strict 
# parsing rules at the model level alongside your examples.

class Category(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, # Automatically removes leading/trailing spaces from strings (e.g., " Electronics " -> "Electronics")
        json_schema_extra={
            "examples": [
                {"name": "Electronics", "description": "Electronic items and gadgets"}
            ]
        }
    )
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: str | None = Field(default=None, max_length=500, description="Category description (optional)")

class Product(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid", # STRICT MODE: If a user sends a field not defined here (like "rating": 5), FastAPI will reject the request.
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "iPhone 15",
                    "price": 999.99,
                    "stock": 50,
                    "category": [{"name": "Electronics", "description": "Electronic items and gadgets"}]
                }
            ]
        }
    )
    id: int = Field(..., gt=0, description="Unique product ID")
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    stock: int | None = Field(default=None, ge=0, description="Available stock (optional)")
    category: list[Category] | None = Field(default=None, description="Product category list (optional)")

class Seller(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {"username": "john_doe", "full_name": "John Doe"}
            ]
        }
    )
    username: str = Field(..., min_length=3, max_length=50, description="Seller username")
    full_name: str | None = Field(default=None, max_length=100, description="Seller full name (optional)")


# =====================================================================
# API Endpoints (Using Way 3 Models: Product, Seller, Category)
# =====================================================================

@app.post('/products')
async def create_product(
    new_product: Product,
    seller: Seller | None,
    sec_key: Annotated[str, Body()] # Expects a raw string 'sec_key' in the JSON body
):
    # Convert the validated Pydantic object into a Python dictionary
    product_dict = new_product.model_dump()
    
    # Perform business logic: calculate total price including 18% tax
    product_with_tax = new_product.price + (new_product.price * 18 / 100)
    product_dict.update({"product_with_tax": product_with_tax})
    
    return {"product": product_dict, "seller": seller, "sec_key": sec_key}       

@app.put('/products/{product_id}')
async def update_product(product_id: int, updated_product_data: Product, discount: float | None = None):
    # This endpoint demonstrates path parameters (product_id), body payloads (updated_product_data), 
    # and optional query parameters (discount).
    return { 
        "product_id": product_id,
        "updated_product_data": updated_product_data,
        "discount": discount
    }
    
@app.post('/product-data')
def post_product_data(product: Annotated[Product, Body(embed=True)]):
    # `embed=True` forces FastAPI to expect the payload wrapped in a JSON key named "product".
    # Example expected request body: { "product": { "id": 1, "name": "iPhone 15", ... } }
    return {"product": product}