"""
Задание №3

Создать API для управления списком задач.

Каждая задача должна содержать поля "название",
"описание" и "статус" (выполнена/не выполнена).

API должен позволять выполнять CRUD операции
с задачами.
"""
import logging
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tasks = [
    {'title': 'Title1', 'description': 'Description 1', 'status': False},
    {'title': 'Title2', 'description': 'Description 2', 'status': False},
    {'title': 'Title3', 'description': 'Description 3', 'status': False},
]

app = FastAPI()


@app.get("/tasks/")
async def read_tasks():
    logger.info('Отработал GET запрос на чтение всего списка задач.')
    return {'tasks': tasks}


def task_check(task_id):
    return task_id < len(tasks)


"""
@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    if task_check(task_id):
        logger.info(f'Отработал GET запрос на чтение одной задачи.')
        return {'task': tasks[task_id]}
    else:
        return {'task': }
"""


"""
@app.post('/tasks/', response_model=Task)
async def create_task(task: Task):
    tasks.append(Task)
    logger.info(f'Отработал POST запрос. Содержимое tasks[]: {tasks}.')
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, new_task: Task):
    tasks[task_id] = new_task
    logger.info(f'Отработал PUT запрос. Содержимое tasks[]: {tasks}.')
    return new_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    remove_item = tasks.pop(task_id)
    logger.info(f'Отработал DELETE запрос. Содержимое tasks[]: {tasks}.')
    return remove_item
"""
