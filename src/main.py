from fastapi import FastAPI
from typing import Union
from helloworld import msg

app = FastAPI()


@app.get("/")
def read_root():
    return {"data": msg}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
