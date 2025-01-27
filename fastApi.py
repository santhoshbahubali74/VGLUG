from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create a FastAPI instance
app = FastAPI()

# Define a model for the items
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory storage for items
items = []

# Create a new item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

# Read all items
@app.get("/items/", response_model=List[Item])
def read_items():
    return items

# Read a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            items.pop(index)
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# To run the app, use: uvicorn your_file_name:app --reload
