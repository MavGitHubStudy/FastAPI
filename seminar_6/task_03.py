"""
Задание №3

Создать API для управления списком задач.

Каждая задача должна содержать поля "название",
"описание" и "статус" (выполнена/не выполнена).

API должен позволять выполнять CRUD операции
с задачами.
"""
import logging
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks = []

app = FastAPI()


class Task(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=200)
    status: bool = Field(default=False)


@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    return tasks[task_id]


@app.post('/tasks/', response_model=Task)
async def create_task(task: Task):
    tasks.append(Task)
    logger.info('Отработал POST запрос. Содержимое tasks[]: {tasks}.')
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, new_task: Task):
    tasks[task_id] = new_task
    return new_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return tasks.pop(task_id)
