# Task API 

A simple CRUD REST API for managing a to-do list, built with FastAPI. Tasks are stored in a SQLite database.

Built for the FlyRank Internship — AI Backend Engeneering Track

## Why SQLite?

SQLite was chosen because it's the simplest way to add real, persistent storage to this project. It needs no separate database server to install or run so there are no extra dependencies. That makes it perfect for a project like this. 

## Where the database is stored

The database is a file named, `tasks.db`, created in the project's root folder. It's created automatically the first time the app runs if it filename doesn't exist. 

## How to start the project

```bash
# Clone the repo and enter it
git clone https://github.com/Ricsmokey/CRUD-API.git
cd CRUD-API


python -m venv venv
venv\Scripts\activate       

# Install dependencies
pip install fastapi uvicorn

#  Run the server
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Interactive Swagger docs are at `http://localhost:8000/docs`. 


## Endpoints

| Method | Path | Description | Success |
|--------|------|-------------|---------|
| GET | `/` | API info | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200 / 404 |
| POST | `/tasks` | Create a task | 201 / 400 |
| PUT | `/tasks/{id}` | Update a task | 200 / 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 / 404 |

## Example SQL query

UPDATE tasks SET done = 1;


## Database viewer

(db-screenshot.png)
