"""
Задание №1

Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.

Создайте модуль приложения и настройте сервер и маршрутизацию.

Создайте класс Task с полями id, title, description и status.

Создайте список tasks для хранения задач.

Создайте маршрут для получения списка задач (метод GET).

Создайте маршрут для создания новой задачи (метод POST).

Создайте маршрут для обновления задачи (метод PUT).

Создайте маршрут для удаления задачи (метод DELETE).

Реализуйте валидацию данных запроса и ответа.
18:55
"""
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool


tasks = []

app = FastAPI()


@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks


@app.post("/tasks/", response_model=Task)
def new_task(task: Task):
    task.id = len(tasks)+1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, new_task: Task):
    for num, task in enumerate(tasks):
        if task.id == task_id:
            new_task.id = task_id
            tasks[num] = new_task
            return new_task
    raise HTTPException(status_code=404, detail='Task {task_id} not fount')



@app.delete('/tasks/{task_id}', response_model=Task)
def delete_task(task_id: int):
    for num, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(num)
    raise HTTPException(status_code=404, detail='Task {task_id} not fount')



if __name__ == "__main__":
    uvicorn.run("task_01:app", host="127.0.0.1", port=8000, reload=True)
