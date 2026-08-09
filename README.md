# Task API

A simple CRUD REST API for managing a to-do list, built with FastAPI. Tasks are stored in memory (no database yet), so data resets when the server restarts.

Built for the FlyRank Internship — Backend Track, Week 2.

## Tech
- Python
- FastAPI
- Uvicorn

## Install & run

```bash
# clone and enter the repo
git clone https://github.com/Ricsmokey/CRUD API.git
cd CRUD API

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       

# install dependencies
pip install "fastapi[standard]"

# run the server
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Interactive Swagger docs at `http://localhost:8000/docs`.

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

