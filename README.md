# Task API

A CRUD To-Do API built with Python and FastAPI, backed by PostgreSQL, and containerized with Docker.

**Assignment Progression:**
- **Assignment 1**: SQLite in-memory storage with REST API fundamentals
- **Assignment 2**: SQLite persistent storage with Git integration
- **Assignment 3**: PostgreSQL database with Docker containerization

This is Assignment 3, which migrates the API from SQLite to a production-ready PostgreSQL database running in Docker containers with Docker Compose orchestration.

## Project Evolution

### A1 → A2: SQLite Implementation
- Task API with 7 REST endpoints
- SQLite database (`tasks.db`) for persistence
- Automatic database initialization with 3 seed tasks
- Comprehensive input validation and error handling

### A2 → A3: PostgreSQL + Docker
- Migrated from SQLite to PostgreSQL (running in Docker)
- Replaced built-in `sqlite3` with `psycopg[binary]` (PostgreSQL driver)
- All parameterized queries for SQL injection prevention
- Docker containerization with single-command deployment
- Environment-driven configuration (credentials in `.env`)
- Docker Compose for multi-container orchestration
- Data persistence via Docker volumes

## Project Objectives (Assignment 3)

This assignment demonstrates:
- Database migration from SQLite to PostgreSQL
- Containerization with Docker
- Multi-container orchestration with Docker Compose
- Environment-based configuration management
- Parameterized queries for security
- One-command deployment workflow
- Git history preservation across major refactors

## Core Features

- **PostgreSQL Database Storage**: Tasks persisted in PostgreSQL running in Docker
- **Automatic Database Setup**: Database schema and seed data created automatically
- **Parameterized Queries**: All SQL uses parameterized format (`%s` placeholders) to prevent SQL injection
- **Docker Containerized**: Full application stack (API + PostgreSQL) runs in containers
- **Docker Compose**: One-command startup: `docker compose up`
- **Environment-Based Config**: Database credentials in `.env` (Git-ignored)
- **Complete CRUD API**: Create, retrieve, update, and delete tasks
- **Automatic Swagger UI**: Full API documentation at `/docs`
- **Proper HTTP Status Codes**: Correct responses for all scenarios

## Technologies Used

- **Python** 3.10+
- **FastAPI** 0.104.1 - Modern web framework for APIs
- **PostgreSQL** (latest) - Production-grade relational database
- **psycopg[binary]** 3.3.5 - PostgreSQL Python driver
- **python-dotenv** 1.2.3 - Environment variable loader
- **Uvicorn** 0.24.0 - ASGI web server
- **Docker** 29.6.1+ - Container runtime
- **Docker Compose** - Multi-container orchestration
- **Swagger UI / OpenAPI** - Automatic API documentation
- **Git & GitHub** - Version control

## API Endpoints

| Method | Endpoint | Description | Success Status |
|--------|----------|-------------|-----------------|
| GET | `/` | Get API metadata and available endpoints | 200 |
| GET | `/health` | Health check endpoint | 200 |
| GET | `/tasks` | Retrieve all tasks | 200 |
| GET | `/tasks/{id}` | Retrieve a specific task by ID | 200 |
| POST | `/tasks` | Create a new task | 201 |
| PUT | `/tasks/{id}` | Update a task (title and/or done status) | 200 |
| DELETE | `/tasks/{id}` | Delete a task | 204 |

## HTTP Status Codes & Validation

- **200 OK** – Successful GET or PUT request
- **201 Created** – Successful task creation (POST)
- **204 No Content** – Successful deletion (DELETE) with empty response body
- **400 Bad Request** – Invalid or missing required fields (empty/whitespace title, missing request body)
- **404 Not Found** – Task ID doesn't exist

## How to Run

### Prerequisites
- Docker 29.6.1 or higher (includes Docker Compose)
- Docker Desktop running
- Git

### Quick Start (One Command)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ehtisham5618/Task-CRUD-API.git
   cd Task-CRUD-API
   ```

2. **Create `.env` file from template**
   ```bash
   cp .env.example .env
   ```

3. **Start the complete stack with one command**
   ```bash
   docker compose up
   ```

   This starts:
   - PostgreSQL container (database)
   - FastAPI container (API server)
   - Shared Docker network for inter-container communication
   - Data volume for persistent storage

4. **Access the API**
   - **API Base URL**: [http://localhost:8000](http://localhost:8000)
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **API Health**: [http://localhost:8000/health](http://localhost:8000/health)

5. **Stop the stack**
   ```bash
   docker compose down
   ```

### Manual Setup (Without Docker)

If you prefer to run locally without Docker:

1. **Clone and navigate**
   ```bash
   git clone https://github.com/ehtisham5618/Task-CRUD-API.git
   cd Task-CRUD-API
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and set DATABASE_URL to your PostgreSQL instance
   ```

3. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

### Environment Variables

The application uses environment variables for configuration (see `.env.example`):

```bash
# Database connection string
DATABASE_URL=postgres://postgres:dev@db:5432/tasks

# PostgreSQL credentials (used by docker-compose)
POSTGRES_PASSWORD=dev
POSTGRES_DB=tasks
```

**Important**: 
- `.env` is Git-ignored (not committed) for security
- `.env.example` is committed as a template for setup
- In Docker Compose, the `db` hostname resolves to the PostgreSQL container
- For local development, replace `db` with `localhost`

## Example cURL Output

Here's a real example of retrieving all tasks from the running API:

```bash
$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Mon, 01 Sep 2026 13:00:00 GMT
server: uvicorn
content-length: 182
content-type: application/json

[
  {"id":1,"title":"Learn FastAPI","done":false},
  {"id":2,"title":"Build a CRUD API","done":false},
  {"id":3,"title":"Deploy to GitHub","done":false}
]
```

### PostgreSQL Verification

With the stack running, you can connect directly to PostgreSQL:

```bash
# Using psql inside the container
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"

# Output:
#  id |       title       | done 
# ----+-------------------+------
#   1 | Learn FastAPI     | f
#   2 | Build a CRUD API  | f
#   3 | Deploy to GitHub  | f
# (3 rows)
```

## Swagger UI

The API includes interactive Swagger documentation available at `/docs`. You can use the **"Try it out"** button to test all endpoints directly from your browser.

Example endpoints visible in Swagger:
- GET `/` – Read Root
- GET `/health` – Health Check
- GET `/tasks` – Get Tasks
- POST `/tasks` – Create Task
- GET `/tasks/{task_id}` – Get Task
- PUT `/tasks/{task_id}` – Update Task
- DELETE `/tasks/{task_id}` – Delete Task

All endpoints include request/response schemas and detailed descriptions.

## Project Structure

```
Task-CRUD-API/
├── main.py                  # FastAPI application with 7 CRUD endpoints
├── database.py              # PostgreSQL connection management
├── Dockerfile              # Docker image definition for API container
├── docker-compose.yaml     # Multi-container orchestration (API + PostgreSQL)
├── requirements.txt        # Python dependencies (FastAPI, Uvicorn, psycopg, python-dotenv)
├── .env.example            # Environment variables template (committed to Git)
├── .env                    # Environment variables (Git-ignored, contains secrets)
├── .gitignore             # Git ignore rules (excludes .env, __pycache__, etc.)
├── .dockerignore          # Docker build context exclusions
├── README.md              # This file
└── docs/
    └── swagger-ui.png     # Swagger UI screenshot
```

### Key Files

**`database.py`** (New in A3)
- `get_db_connection()`: Establishes PostgreSQL connection with retry logic
- `init_db()`: Creates tables and seeds initial data on startup

**`Dockerfile`** (New in A3)
- Python 3.11-slim base image
- Installs requirements
- Exposes port 8000
- Runs uvicorn on `0.0.0.0` for Docker network access

**`docker-compose.yaml`** (New in A3)
- Defines `db` service (PostgreSQL)
- Defines `api` service (FastAPI)
- Configures volumes for data persistence
- Sets up health checks
- Manages environment variables

**`.env.example`** (New in A3)
- Template for environment variables
- Includes placeholder credentials
- Committed to Git for documentation

**`.env`** (New in A3)
- Actual environment variables with real credentials
- Git-ignored for security
- Created from `.env.example` during setup

## Database (PostgreSQL)

### Architecture

The API uses PostgreSQL (a production-grade relational database) running in a Docker container. Docker Compose manages both the database and API containers.

```
┌─────────────────────────────────┐
│   docker-compose network        │
├─────────────────────────────────┤
│  api:8000 (FastAPI container)   │
│      ↓ (connects via "db")      │
│  db:5432 (PostgreSQL container) │
│      ↓ (persistent volume)      │
│  taskdata (Docker volume)       │
└─────────────────────────────────┘
```

### Automatic Initialization

When `docker compose up` starts, the database is automatically initialized:

1. PostgreSQL container starts
2. Database `tasks` is created if not present
3. Table `tasks` is created with proper schema:
   ```sql
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       done BOOLEAN NOT NULL DEFAULT FALSE
   );
   ```
4. Three seed tasks are inserted (only if table is empty)
5. Data persists via `taskdata` volume across container restarts

### Querying the Database

While the stack is running, you can query PostgreSQL:

```bash
# Connect to the PostgreSQL container
docker exec -it taskdb psql -U postgres -d tasks

# Inside psql prompt:
\dt                    # List tables
SELECT * FROM tasks;   # View all tasks
SELECT COUNT(*) FROM tasks;  # Count tasks
\q                     # Exit psql
```

### Parameterized Queries

All SQL queries use parameterized format (`%s` placeholders) via psycopg to prevent SQL injection:

```python
# Example: Safe query with parameters
cursor.execute(
    "SELECT id, title, done FROM tasks WHERE id = %s",
    (task_id,)  # Parameter passed separately
)
```

### Data Persistence

- Data is stored in the `taskdata` Docker volume
- Volume survives container restarts and `docker compose down` (data persists)
- To reset data, run: `docker volume rm task1_taskdata`
- Then restart: `docker compose up` (creates new volume with seed data)

## Author

**Ehtisham Abid**

---

**Happy coding!** 🚀
