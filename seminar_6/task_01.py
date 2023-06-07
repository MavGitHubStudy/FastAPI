"""
Задание №1

Разработать API для управления списком пользователей
с использованием базы данных SQLite. Для этого создайте
модель User со следующими полями:

- id: int (идентификатор пользователя, генерируется
  автоматически)

- username: str (имя пользователя)

- email: str (электронная почта пользователя)

- password: str (пароль пользователя)
"""
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///task_01.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


class UserIn(BaseModel):
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class User(BaseModel):
    # id: int = Field(default=None, alias="user_id")
    id: int
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


# @app.get("/fake_users/{count}")
# async def create_note(count: int):
#     for i in range(1, count + 1):
#         query = users.insert().values(username=f'user{i}',
#                                       email=f'mail{i}@mail.ru',
#                                       password=f'password{i}')
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}

@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    # query = users.insert().values(username=user.name,
    #                               email=user.email,
    #                               password=user.password)
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(
        **new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
