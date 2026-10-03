from fastapi import FastAPI, Cookie
from typing import Annotated
from pydantic import BaseModel, Field , ConfigDict

app = FastAPI()

## cookie parameter
@app.get("/products/recommendations")
async def get_recommendations(session_id: Annotated[str|None, Cookie()] = None):
    if session_id: 
        return {"message": f"recommendations for session {session_id}", "session_id": session_id}
    else:
        return {"message": "session id not Provided"}


### for api tets run this curl in cmd
"""
curl -X GET "http://127.0.0.1:8000/products/recommendations" -H "accept: */*" -H "Cookie: session_id=java"
"""




##### Cookies  Using Pydentic Model
class ProductCookies(BaseModel):
    model_config = ConfigDict(
            extra="forbid",            # Rejects any unexpected or extra cookie fields (Security)
            str_strip_whitespace=True  # Automatically removes leading/trailing spaces from string inputs
        )

    session_id:str
    prefered_catagory: str| None = None
    tracking_id: str|None = None


@app.get("/products_2/recommendations")
async def get_recommendations(cookies: Annotated[ProductCookies, Cookie()]):
    response = {}
    if cookies.session_id: 
        response = {
            "message": f"recommendations for session {cookies.session_id}", 
            "session_id": cookies.session_id
        }
    elif cookies.prefered_catagory:
        response = {
            "message": f"recommendations for category {cookies.prefered_catagory}"
        }
    else:
        response = {
            "message": "session id not Provided"
        }
    return response


##  curl
"""
curl -X GET "http://127.0.0.1:8000/products_2/recommendations" -H "Cookie: session_id=java123; prefered_catagory=electronics"
"""