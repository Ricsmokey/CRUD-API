import sqlite3
from fastapi import HTTPException


def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    tasks = cursor.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return [dict(task) for task in tasks]


def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    tasks = cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    if tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(tasks)


def create_task(title, done=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (title, done))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "title": title, "done": done}


def update_task(task_id, title, done):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ?, done = ? WHERE id = ?', (title, done, task_id))
    conn.commit()
    updated_task = cursor.rowcount
    conn.close()
    if updated_task == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "title": title, "done": done}


def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    deleted_task = cursor.rowcount
    conn.close()
    if deleted_task == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id}