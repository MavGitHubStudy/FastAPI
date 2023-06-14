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
"""
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

tasks = []


class Task(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(max_length=50)
    description: str = Field(max_length=100)
    status: bool = Field(default=False)


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for obj in tasks:
        if obj.id == task_id:
            return obj
    raise HTTPException(status_code=404, detail=f'Task {obj} not fount')


@app.post("/tasks_list/")
async def fake_tasks():
    for i in range(1, 10 + 1):
        new_task = {"id": i, "title": f"title{i}", "description": f"description{i}", "status": False}
        tasks.append(new_task)
    return tasks


@app.post("/tasks/", response_model=Task)
async def add_task(task: Task):
    task.id = len(tasks)+1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, new_task: Task):
    for _num, _task in enumerate(tasks):
        if _task.id == task_id:
            new_task.id = task_id
            tasks[_num] = new_task
            return new_task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not fount')


@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    for _num, _task in enumerate(tasks):
        if _task.id == task_id:
            return tasks.pop(_num)
    raise HTTPException(status_code=404, detail=f'Task {task_id} not fount')


if __name__ == "__main__":
    uvicorn.run("task_08:app", host="127.0.0.1", port=8000, reload=True)
