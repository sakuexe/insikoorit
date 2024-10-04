from fastapi import FastAPI
from typing import Union
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
