"""
Промежуточная аттестация

Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы
и пользователи.

- Таблица "Товары" должна содержать информацию о доступных товарах, их описаниях и ценах.

- Таблица "Заказы" должна содержать информацию о заказах, сделанных пользователями.

- Таблица "Пользователи" должна содержать информацию о зарегистрированных пользователях магазина.

* Таблица пользователей должна содержать следующие поля: id(PRIMARY_KEY), имя, фамилия, адрес электронной почты
  и пароль.

* Таблица заказов должна содержать следующие поля: id (PRIMARY_KEY), id пользователя (FOREIGN KEY),
  id товара (FOREIGN KEY), дата заказа и статус заказа.

* Таблица товаров должна содержать следующие поля: id (PRIMARY_KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.

Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
"""
# from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///online_store.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("p_name", sqlalchemy.String(128)),
    sqlalchemy.Column("p_description", sqlalchemy.String(200)),
    sqlalchemy.Column("p_price", sqlalchemy.Float),
)


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("u_name", sqlalchemy.String(50)),
    sqlalchemy.Column("u_surname", sqlalchemy.String(50)),
    sqlalchemy.Column("u_email", sqlalchemy.String(128)),
    sqlalchemy.Column("u_password", sqlalchemy.String(50)),
)


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("u_idr", sqlalchemy.Integer),
    sqlalchemy.Column("p_id", sqlalchemy.Integer),
    sqlalchemy.Column("o_date", sqlalchemy.DateTime),
    sqlalchemy.Column("o_status", sqlalchemy.String(50)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


"""
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
"""
