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





# Task API — Containerized with Postgres

A CRUD REST API for managing a to-do list, built with FastAPI. Tasks are stored in a **PostgreSQL** database runs in Docker with a single command.

Built for the FlyRank Internship.


## Run it — one command

You need [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash

git clone https://github.com/Ricsmokey/CRUD-API.git
cd CRUD-API

cp .env.example .env

docker compose up --build
```
## Live App
`http://localhost:8003`, with interactive Swagger UI
`http://localhost:8003/docs`. 


## Configuration

Configuration comes from a `.env` file (git-ignored — never committed). A template is provided in `.env.example`; copy it to `.env` before running.

The one variable:
`.env.example` is committed so anyone cloning knows which variables to set


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


## Example request

curl.exe -i http://localhost:8003/tasks/1

## Persistence

Data persists across restarts because Postgres stores its data in a Docker **volume** (`taskdata`). Verified by: creating a task via the API, running `docker compose down`, then `docker compose up` again — the created task was still present in `GET /tasks`.


## Database screenshot

![Tasks in Postgres](db-screenshot.png)