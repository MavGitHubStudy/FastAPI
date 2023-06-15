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

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class Task(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(max_length=50)
    description: str = Field(max_length=100)
    status: bool = Field(default=False)


tasks: List[Task] = []


@app.get("/fake_tasks/{count}")
async def create_note(count: int):
    for i in range(count):
        new_task = Task(id=i, title=f"Title{i}", description=f"Description{i}", status=False)
        tasks.append(new_task)
    return {'message': f'{count} fake tasks created'}


@app.get("/tasks/", response_model=List[Task])
async def task_list():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def task_detail(task_id: int):
    for _task in tasks:
        # if _task['id'] == task_id:
        if _task.id == task_id:
            return _task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.post("/tasks", response_model=Task)
async def task_add(task: Task):
    task.id = len(tasks)
    tasks.append(task)
    return tasks[-1]


@app.put("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, new_task: Task):
    if not tasks[task_id]:
        raise HTTPException(status_code=404, detail=f'Task {task_id} not found')
    new_task.id = task_id
    tasks[task_id] = new_task
    return tasks[task_id]


@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    if not tasks[task_id]:
        raise HTTPException(status_code=404, detail=f'Task {task_id} not found')
    return tasks.pop(task_id)


if __name__ == "__main__":
    uvicorn.run("task_08:app", host="127.0.0.1", port=8000, reload=True)
