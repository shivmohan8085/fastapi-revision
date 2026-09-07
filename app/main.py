from fastapi import FastAPI , status , Query
from enum import Enum

app = FastAPI()

PRODUCTS = [
    {
        "id": 1,
        "title": "Wireless Bluetooth Headphones",
        "price": 1499,
        "description": "High-quality wireless headphones with noise cancellation and long battery life."
    },
    {
        "id": 2,
        "title": "Smart Watch",
        "price": 2499,
        "description": "Feature-rich smartwatch with fitness tracking, heart-rate monitoring, and notifications."
    },
    {
        "id": 3,
        "title": "Mechanical Keyboard",
        "price": 3299,
        "description": "RGB mechanical keyboard with tactile switches, suitable for gaming and programming."
    },
    {
        "id": 4,
        "title": "Wireless Mouse",
        "price": 899,
        "description": "Ergonomic wireless mouse with adjustable DPI and comfortable grip."
    },
    {
        "id": 5,
        "title": "USB-C Fast Charger",
        "price": 799,
        "description": "Compact 65W USB-C fast charger compatible with phones, tablets, and laptops."
    },
    {
        "id": 6,
        "title": "Laptop Stand",
        "price": 1299,
        "description": "Adjustable aluminum laptop stand designed for better posture and improved airflow."
    },
    {
        "id": 7,
        "title": "Portable Bluetooth Speaker",
        "price": 1799,
        "description": "Compact Bluetooth speaker with powerful sound, deep bass, and water resistance."
    },
    {
        "id": 8,
        "title": "Webcam Full HD",
        "price": 1599,
        "description": "1080p Full HD webcam with built-in microphone for meetings, streaming, and video calls."
    },
    {
        "id": 9,
        "title": "External SSD 1TB",
        "price": 6499,
        "description": "Fast 1TB portable SSD for storing and transferring large files quickly."
    },
    {
        "id": 10,
        "title": "Gaming Controller",
        "price": 2199,
        "description": "Ergonomic wireless gaming controller with responsive buttons and dual vibration feedback."
    }
]



  



@app.get('/')
def home():
  return {"mesaage":"hello this is fastapi"}



# get request
# read and fetch all data
@app.get('/products', status_code=status.HTTP_200_OK)
async def all_products(search:str|None = Query(default=None, max_length=5) ): # query validation
  if search:
      search_lower= search.lower()
      filtered_productus = []
      for productus in PRODUCTS:
        if search_lower in productus['title'].lower():
          filtered_productus.append(productus)
      return filtered_productus
  return PRODUCTS


# Read and fetch single data
@app.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def get_product(product_id:int):
  # return {'response':'product details', 'product_id':product_id}
  for product in PRODUCTS:
    if product['id'] == product_id:
      return product
    
    

@app.post('/products', status_code=status.HTTP_201_CREATED)
async def add_product(new_product:dict):
  # return {'response':'product created', 'product':product}
  PRODUCTS.append(new_product)
  return {'response':'product created', 'new_product':new_product}
  



@app.put('/products/{product_id}')
async def update_product(updated_product:dict , product_id:int):
  # return {'response':'product updated successfully', 'updated_product':updated_product,  'product_id':product_id}
  for index , product in enumerate(PRODUCTS):
    if product['id'] == product_id:
      PRODUCTS[index] = updated_product    
  return {'response':'product updated successfully', 'updated_product':updated_product,  'product_id':product_id}
  



@app.patch('/products/{product_id}')
async def partial_update_product(partially_updated_product_data:dict , product_id:int):
  # return {'response':'product partially updated successfully', 'partially_updated_product':partially_updated_product,  'product_id':product_id}
  for index , product in enumerate(PRODUCTS):
    if product['id'] == product_id:
      product.update(partially_updated_product_data)
  return {'response':'product partially updated successfully', 'partially_updated_product':partially_updated_product_data,  'product_id':product_id}


@app.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id:int):
  # return {'response':'product deleted', 'product_id':product_id}
  for index , product in enumerate(PRODUCTS):
    if product['id'] == product_id:
      PRODUCTS.pop(index)

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





#-------------------------------------------------------
#                 Query Parameter
#-------------------------------------------------------

@app.get('/product-type')
async def get_product_type(catagory:str|None= None, limit:int|None = None):
  return {"status":"OK", "catagory":catagory, "limit":limit}