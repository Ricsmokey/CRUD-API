import os

from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        cursor.execute("SELECT COUNT(*) AS count FROM tasks")
        if cursor.fetchone()["count"] == 0:
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                [("Buy a car", False), ("Clean the house", True), ("Finish the assignment", False)]
            )
    conn.commit()
    conn.close()

def get_db_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_all():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks ORDER BY id")
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
    conn.close()
    return row

def create_task(title, done=False):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (title, done))
        task_id = cursor.fetchone()["id"]
        conn.commit()
    conn.close()
    return {"id": task_id, "title": title, "done": done}


def update_task(task_id, title, done):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s", (title, done, task_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
    conn.close()
    return {"id": task_id, "title": title, "done": done}


def delete_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
    conn.close()
    return {"id": task_id}
