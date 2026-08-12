from itertools import count
from tkinter import INSERT

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import seed

# Create SQLite database
db = "tasks.db"
def get_db_connection():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
)
""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]
if count == 0:
    tasks = [("Buy a car", False), ("Clean the house", True), ("Finish the assignment", False)]
    cursor.executemany("INSERT OR IGNORE INTO tasks (title, done) VALUES (?, ?)", tasks)
    print("Table 'tasks' seeded with initial data.")
    conn.commit()
else:
    print("Table 'tasks' already has data. Skipping seeding.")
    cursor.close()
    conn.close()


app = FastAPI(title ="Todo List API")
@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return {"status": "ok"}


# Pydantic models
class CreateTask(BaseModel):
    title: str

class Task(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    

# Get tasks
@app.get("/tasks")
async def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    tasks = [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]
    cursor.close()
    conn.close()
    return tasks

# Get task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail={ "error": "Task not found"})
    
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}



# Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: CreateTask):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, False))
    conn.commit()
    task_id = cursor.lastrowid
    cursor.close()
    conn.close()

    if task_id is None:
        raise HTTPException(status_code=400, detail={ "error": "Missing Title"})
    return {"id": task_id, "title": task.title, "done": False}




# Update and Delete
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: UpdateTask):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail={ "error": "Task not found"})

    updated_title = task.title if task.title is not None else row["title"]
    updated_done = task.done if task.done is not None else bool(row["done"])

    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (updated_title, updated_done, task_id))
    conn.commit()
    cursor.close()
    conn.close()

    return {"id": task_id, "title": updated_title, "done": updated_done}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail={ "error": "Task not found"})

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

    