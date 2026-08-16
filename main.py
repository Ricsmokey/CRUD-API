import repository
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

repository.init_db()

app = FastAPI(title="Todo List API")


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def health():
    return {"status": "ok"}


# Pydantic models
class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/tasks")
def get_tasks():
    return repository.get_all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repository.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
    return task


@app.post("/tasks", status_code=201)
def create_task(task: CreateTask):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
    return repository.create_task(task.title)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: UpdateTask):
    existing = repository.get_task(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
    title = task.title if task.title is not None else existing["title"]
    done = task.done if task.done is not None else existing["done"]
    return repository.update_task(task_id, title, done)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if repository.delete_task(task_id) is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})