from fastapi import FastAPI, Request
import asyncio
import time
from pydantic import BaseModel
import logging

### Run with: uvicorn fast_api_app:app --host 0.0.0.0 --port 8080
logging.basicConfig(
    level=logging.INFO,  # Set the default log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to STDOUT (which Docker captures)
)

# Get the logger for this module
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/ping")
async def delayed_response():
    await asyncio.sleep(2)  # Simulate a delay of 2 seconds
    return {"message": "This response was delayed by 2 seconds"}

@app.get("/hello")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/submit/")
async def submit_data(request: Request):
    body = await request.json()
    # Now you can access the data in `body` dictionary
    return {"received_data": body}

class Item(BaseModel):
    name: str
    description: str

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_description": item.description}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    logger.info(f"Updating item {item_id} with name: {item.name} and description: {item.description}")
    return {"item_id": item_id, "item_name": item.name, "item_description": item.description}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    logger.info(f"Deleting item {item_id}")
    return {"message": f"Item {item_id} deleted"}

@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name, "item_description": item.description}