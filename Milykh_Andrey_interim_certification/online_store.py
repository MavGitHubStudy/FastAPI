"""
Промежуточная аттестация

Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трёх таблиц: товары, заказы и пользователи.

- Таблица "Товары" должна содержать информацию о доступных товарах, их описаниях
  и ценах.

- Таблица "Заказы" должна содержать информацию о заказах, сделанных
  пользователями.

- Таблица "Пользователи" должна содержать информацию о зарегистрированных
  пользователях магазина.

* Таблица пользователей должна содержать следующие поля: id(PRIMARY_KEY), имя,
  фамилия, адрес электронной почты и пароль.

* Таблица заказов должна содержать следующие поля: id (PRIMARY_KEY),
  id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
  заказа.

* Таблица товаров должна содержать следующие поля: id (PRIMARY_KEY), название,
  описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД
для каждой из трёх таблиц.

Реализуйте CRUD операции для каждой из таблиц через создание маршрутов,
REST API.
"""
import enum
import databases
from random import randint, random
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, \
    Float, DateTime, ForeignKey, create_engine
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

DATABASE_URL = "sqlite:///online_store.db"

database = databases.Database(DATABASE_URL)

metadata = MetaData()


products = Table(
    "products",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("p_name", String(128), nullable=False),
    Column("p_description", String(200), nullable=False),
    Column("p_price", Float(), nullable=False),
)


users = Table(
    "users",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("u_name", String(50), nullable=False),
    Column("u_surname", String(50), nullable=False),
    Column("u_email", String(128), nullable=False),
    Column("u_password", String(50), nullable=False),
)


orders = Table(
    "orders",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("u_id", ForeignKey("users.id")),
    Column("p_id", ForeignKey("products.id")),
    Column("o_date", DateTime(), default=datetime.utcnow),
    Column("o_status", Integer, default=0),
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


class UserIn(BaseModel):
    u_name: str = Field(max_length=50)
    u_surname: str = Field(max_length=50)
    u_email: str = Field(max_length=128)
    u_password: str = Field(max_length=50)


class User(BaseModel):
    # id: int = Field(default=None, alias="user_id")
    id: int
    u_name: str = Field(max_length=50)
    u_surname: str = Field(max_length=50)
    u_email: str = Field(max_length=128)
    u_password: str = Field(max_length=50)


class ProductIn(BaseModel):
    p_name: str = Field(max_length=128)
    p_description: str = Field(max_length=200)
    p_price: float


class Product(BaseModel):
    id: int
    p_name: str = Field(max_length=128)
    p_description: str = Field(max_length=200)
    p_price: float


class OrderState(enum.Enum):
    created = (0, "Создан")
    paid = (1, "Оплачен")
    collected = (2, "Собран")
    send = (3, "Отправлен")
    received = (4, "Получен")


class OrderIn(BaseModel):
    u_id: int
    p_id: int
    o_date: datetime
    o_status: int


class Order(BaseModel):
    id: int
    u_id: int
    p_id: int
    o_date: datetime
    o_status: int


# Start Методы для генерации тестовых данных в базе данных
"""
# Для теста выбирал count=25 
# http://127.0.0.1:8000/fake_users/25
@app.get("/fake_users/{count}")
async def create_note_users(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(u_name=f'Name{i}',
                                      u_surname=f'Surname{i}',
                                      u_email=f'mail{i}@mail.ru',
                                      u_password=f'password{i}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


# Для теста выбирал count=30
# http://127.0.0.1:8000/fake_products/30
@app.get("/fake_products/{count}")
async def create_note_products(count: int):
    for i in range(1, count + 1):
        _number_float = random() * 100
        _price = round(_number_float, 2)
        query = products.insert().values(p_name=f'ProductName{i}',
                                         p_description=f'ProductDescription{i}',
                                         p_price=_price)
        await database.execute(query)
    return {'message': f'{count} fake products create'}


# Для теста выбирал count=45
# http://127.0.0.1:8000/fake_orders/45
@app.get("/fake_orders/{count}")
async def create_note_orders(count: int):
    for i in range(1, count + 1):
        query = orders.insert().values(u_id=randint(1, 25),
                                       p_id=randint(1, 30),
                                       o_date=datetime.utcnow(),
                                       o_status=0)
        await database.execute(query)
    return {'message': f'{count} fake orders create'}
"""
# End Методы для генерации тестовых данных в базе данных


# --- Start Методы получения содержимого таблиц базы данных ---
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)
# --- End Методы получения содержимого таблиц базы данных ---


# --- Start Методы получения элемента таблиц базы данных по id ---
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)
# --- End Методы получения элемента таблиц базы данных по id ---


# --- Start Методы добавления элемента таблиц базы данных ---
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    # query = users.insert().values(u_name=user.u_name,
    #                               u_surname=user.u_surname,
    #                               u_email=user.u_email,
    #                               u_password=user.u_password)
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}
# --- End Методы добавления элемента таблиц базы данных ---


# --- Start Методы обновления элемента таблиц базы данных ---
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(
        **new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(
        **new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(
        **new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}
# --- End Методы обновления элемента таблиц базы данных ---


# --- Start Методы удаления элемента таблиц базы данных по id ---
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}


@app.delete("/orders/{orer_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
# --- End Методы удаления элемента таблиц базы данных по id ---
