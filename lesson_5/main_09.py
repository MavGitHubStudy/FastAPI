"""
Конечная точка API - это URL-адрес, по которому
клиент может отправлять запросы к серверу. В FastAPI
определение конечных точек происходит с помощью
декораторов.
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def create_item(item_id: int):
    return {"item_id": item_id}
