from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()


class Item(BaseModel):
   name : str 
   phone_number : int 
   address : str | None=Field(default=None,strict=True)

@app.get("/health")
async def get_health():
  return {"status":"healthy"}

@app.post("/echo")
async def post_data(item:Item):
    return item
