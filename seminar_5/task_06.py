"""
Задание №6

Создать веб-страницу для отображения списка пользователей.
Приложение должно использовать шаблонизатор Jinja для
динамического формирования HTML страницы.

Создайте модуль приложения и настройте сервер и маршрутизацию.

Создайте класс User с полями id, name, email и password.

Создайте список users для хранения пользователей.

Создайте HTML шаблон для отображения списка пользователей.
Шаблон должен содержать заголовок страницы, таблицу со
списком пользователей и кнопку для добавления
нового пользователя.

Создайте маршрут для отображения списка пользователей
(метод GET).

Реализуйте вывод списка пользователей через шаблонизатор Jinja.
01:18:30
"""
# from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
# from random import choice

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []

for i in range(1, 11):
    user = User(id=i,
                name=f'name{i}',
                email=f'email{1}@mail.ru',
                password=f'password{i}')
    users.append(user)


@app.get("/users/", response_class=HTMLResponse)
def get_users(request: Request):
    return templates.TemplateResponse('user.html',
                                      {'request': request,
                                       'users': users})


@app.post("/users/", response_model=User)
def new_user(_user: User):
    _user.id = len(users)+1
    users.append(_user)
    return _user


@app.put("/users/{user_id}", response_model=User)
def edit_user(_user_id: int, _edit_user: User):
    for _num, _user in enumerate(users):
        if user.id == _user_id:
            _edit_user.id = _user_id
            users[_num] = _edit_user
            return _edit_user
    raise HTTPException(status_code=404, detail='User {_user_id} not fount')


@app.delete('/users/{user_id}', response_model=User)
def delete_user(_user_id: int):
    for _num, _user in enumerate(users):
        if _user.id == _user_id:
            return users.pop(_num)
    raise HTTPException(status_code=404, detail='User {_user_id} not fount')


if __name__ == "__main__":
    uvicorn.run("task_06:app", host="127.0.0.1", port=8000, reload=True)
