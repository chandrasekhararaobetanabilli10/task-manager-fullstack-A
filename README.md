# Personal Task Manager — Full Stack

A beginner-friendly CRUD app with a browser UI, Flask REST API, and MySQL database.

## Features
- Add, view, edit, and delete tasks
- Optional due dates
- Pending and Completed statuses
- Filter tasks by status
- MySQL named volume for persistent data

## Run with Docker (recommended)
Requirements: Docker Engine and Docker Compose. From this folder run:

```bash
sudo docker compose up -d --build
```

Open http://localhost:5000

Useful commands:

```bash
sudo docker compose ps
sudo docker compose logs -f web
sudo docker compose down
```

`docker compose down` keeps database data in its named volume. `sudo docker compose down -v` deletes that data too.

## Run locally
1. Start MySQL and execute `database/schema.sql`.
2. Install dependencies: `pip install -r backend/requirements.txt`.
3. Set DB_HOST, DB_PORT, DB_NAME, DB_USER and DB_PASSWORD environment variables as needed.
4. Run `cd backend && python app.py`.
5. Open http://localhost:5000.

## API
- GET `/api/tasks` — list tasks
- POST `/api/tasks` — create task
- PUT `/api/tasks/<id>` — update task
- DELETE `/api/tasks/<id>` — delete task

## Structure
- `frontend/` — HTML, CSS, JavaScript
- `backend/` — Flask backend
- `database/` — MySQL schema
- `Dockerfile`, `compose.yaml` — Docker setup

The example credentials are for local learning only. Change them before deploying publicly.
