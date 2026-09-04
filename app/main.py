from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get('/')
def home():
  return {"mesaage":"hello this is fastapi"}



# get request
# read and fetch all data
@app.get('/products')
async def all_products():
  return {"response":"All products"}


# Read and fetch single data
@app.get('/products/{product_id}')
async def get_product(product_id:int):
  return {'response':'product details', 'product_id':product_id}

@app.post('/products')
async def add_product(product:dict):
  return {'response':'product created', 'product':product}



@app.put('/products/{product_id}')
async def update_product(updated_product:dict , product_id:int):
  return {'response':'product updated successfully', 'updated_product':updated_product,  'product_id':product_id}



@app.patch('/products/{product_id}')
async def partial_update_product(partially_updated_product:dict , product_id:int):
  return {'response':'product partially updated successfully', 'partially_updated_product':partially_updated_product,  'product_id':product_id}


@app.delete('/products/{product_id}')
async def delete_product(product_id:int):
  return {'response':'product deleted', 'product_id':product_id}
  
  
  
  
  
  ## in parameter predefined values
class ProductCatagory(str, Enum):
    books ="books"
    phones = "phones"
    
@app.get('/products-catagory/{catagory}')
async def get_catagory(catagory:ProductCatagory):
  return {"ProductCatagory" : catagory}
  
  
  
  
  
  
# file path
@app.get("/file/{path:path}")
async def get_file_path(path: str):
  return {"path":path}
