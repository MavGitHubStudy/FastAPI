"""
Задание №8

Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать
статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:

- GET/tasks - возвращает список всех задач.

- GET/tasks/{id} - возвращает задачу с указанным
  идентификатором.

- POST/tasks - добавляет новую задачу.

- PUT/tasks/{id} - обновляет задачу с указанным
  идентификатором

- DELETE/tasks/{id} - удаляет задачу с указанным
  идентификатором.

Для каждой конечной точки необходимо проводить
валидацию данных запроса и ответа. Для этого
использовать библиотеку Pydantic.

https://www.vultr.com/docs/how-to-create-a-restful-api-using-python-and-fastapi-3398/
"""
from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
templates = Jinja2Templates(directory='templates')

tasks = [
    {'id': 0, 'title': 'task0', 'description': 'description0', 'status': False},
    {'id': 1, 'title': 'task1', 'description': 'description1', 'status': False},
    {'id': 2, 'title': 'task2', 'description': 'description2', 'status': False},
    {'id': 3, 'title': 'task3', 'description': 'description3', 'status': False},
]


class Task(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(max_length=50)
    description: str = Field(max_length=100)
    status: bool = Field(default=False)


@app.get("/tasks/")
async def task_list():
    return {'tasks': tasks}


def task_exist_check(task_id):
    if not tasks[task_id]:
        raise HTTPException(status_code=404,
                            detail=f'Task with id={task_id} Not Found')


def task_not_exist_check(task_id):
    if tasks[task_id]:
        raise HTTPException(status_code=404,
                            detail=f'Task with id={task_id} Found')


@app.get("/tasks/{task_id}")
async def task_detail(task_id: int):
    task_exist_check(task_id)
    return {'task': tasks[task_id]}


@app.post("/tasks")
async def task_add(task: Task):
    task_not_exist_check(task.id)
    tasks.append(task)
    return {'task': tasks[-1]}


@app.put("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, new_task: Task):
    for _num, _task in enumerate(tasks):
        if _task[id] == task_id:
            new_task.id = task_id
            tasks[_num] = new_task
            return new_task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    for _num, _task in enumerate(tasks):
        if _task.id == task_id:
            return tasks.pop(_num)
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


if __name__ == "__main__":
    uvicorn.run("task_08:app", host="127.0.0.1", port=8000, reload=True)
