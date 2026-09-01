# Task API / Polite Scraper

A CRUD To-Do API built with Python and FastAPI, backed by PostgreSQL, containerized with Docker, secured with Supabase Auth — and extended with a polite web scraping pipeline.

**Assignment Progression:**
- **Assignment 1**: In-memory CRUD API with REST fundamentals
- **Assignment 2**: SQLite persistent storage with Git integration
- **Assignment 3**: PostgreSQL database with Docker containerization
- **Assignment 4**: Supabase Auth with JWT-based protected routes
- **Assignment 5**: Polite web scraping pipeline with caching and Pydantic validation

The API work (A1–A4) lives at the repository root. The scraper (A5) lives in `scraper/`.

## Project Evolution

### A1 -> A2: SQLite Implementation
- Task API with 7 REST endpoints
- SQLite database (`tasks.db`) for persistence
- Automatic database initialization with seed tasks
- Input validation and error handling

### A2 -> A3: PostgreSQL + Docker
- Migrated from SQLite to PostgreSQL running in Docker
- Replaced built-in `sqlite3` with `psycopg[binary]`
- Docker Compose orchestration for API + database
- Environment-driven configuration through `.env`
- Persistent PostgreSQL data through Docker volumes

### A3 -> A4: Authentication with Supabase Auth
- Signup and login handled by Supabase Auth
- Access tokens verified by FastAPI through Supabase
- Protected routes using reusable FastAPI dependency injection
- HTTPBearer security scheme for Swagger UI
- Existing task CRUD endpoints remain public and unchanged

### A4 -> A5: The Polite Scraper
- Separate `scraper/` project within the same repository
- Scrapes first 3 catalogue pages of Books to Scrape (60 books)
- Caching, 500 ms politeness delay, HTTP status checking
- Pydantic validation, `books.json`, `errors.json`, `run-report.json`
- `--test-failure` mode demonstrates one-page failure resilience

## Project Objectives (Assignment 4)

This assignment demonstrates:
- Third-party authentication provider integration
- Bearer token protection for selected API routes
- Reusable FastAPI auth dependency
- Swagger UI bearer authorization
- Separation between public and protected endpoints
- Safe handling of secrets through environment variables

## Core Features

- **User Authentication**: Signup and login via Supabase Auth
- **JWT Access Tokens**: Bearer token authorization for protected routes
- **Server-Side Verification**: FastAPI verifies access tokens through Supabase
- **Reusable Auth Dependency**: One shared guard protects all auth-required routes
- **Public Routes**: Existing CRUD routes and `/public/info` remain unauthenticated
- **PostgreSQL Database**: Persistent task storage
- **Docker Compose**: One command starts the API and PostgreSQL stack
- **Swagger UI**: Interactive docs with bearer-auth locks on protected routes

## Technologies Used

- **Python** 3.10+
- **FastAPI** 0.104.1
- **Supabase Auth**
- **Supabase Python SDK** 2.31.0
- **PostgreSQL**
- **psycopg[binary]** 3.3.5
- **python-dotenv** 1.2.3
- **Uvicorn** 0.24.0
- **Docker** and **Docker Compose**
- **HTTPBearer** from FastAPI security
- **Swagger UI / OpenAPI**
- **Git & GitHub**

## API Endpoints

### Task Management (CRUD)

| Method | Endpoint | Description | Authentication | Success |
|--------|----------|-------------|----------------|---------|
| GET | `/` | Get API metadata | No | 200 |
| GET | `/health` | Health check | No | 200 |
| GET | `/tasks` | Retrieve all tasks | No | 200 |
| GET | `/tasks/{id}` | Retrieve a specific task | No | 200 |
| POST | `/tasks` | Create a new task | No | 201 |
| PUT | `/tasks/{id}` | Update a task | No | 200 |
| DELETE | `/tasks/{id}` | Delete a task | No | 204 |

### Authentication Routes

| Method | Endpoint | Purpose | Authentication | Success |
|--------|----------|---------|----------------|---------|
| POST | `/auth/signup` | Create account | No | 201 |
| POST | `/auth/login` | Login and receive tokens | No | 200 |
| POST | `/auth/logout` | End authenticated session | Bearer token | 204 |
| GET | `/public/info` | Public information | No | 200 |
| GET | `/protected/profile` | Current user profile | Bearer token | 200 |
| GET | `/protected/dashboard` | Demonstrates reusable auth protection | Bearer token | 200 |

`/protected/dashboard` is intentionally minimal. It exists only to demonstrate that the same auth dependency can protect more than one route.

## HTTP Status Codes

- **200 OK**: Successful GET, PUT, or login request
- **201 Created**: Successful signup or task creation
- **204 No Content**: Successful delete or logout with an empty response body
- **400 Bad Request**: Missing or invalid required request data
- **401 Unauthorized**: Missing, malformed, invalid, or expired bearer token
- **404 Not Found**: Requested task does not exist

## Authentication Overview

The auth flow is:

```text
Signup/Login -> Supabase Auth -> access token -> Bearer token -> FastAPI verification
```

Supabase manages user accounts, passwords, password hashing, and token creation. This backend does not store passwords, create JWTs, sign tokens, or manually verify JWT signatures. Protected routes call Supabase to verify the received access token.

## How to Run

### Prerequisites

- Docker Desktop with Docker Compose
- Git
- A Supabase project

### Supabase Setup

1. Create a free Supabase project at https://supabase.com.
2. Open **Project Settings -> API**.
3. Copy the project URL.
4. Copy the **publishable key** or legacy **anon public key**.
5. Put both values in `.env`.
6. For this assignment demo, disable email confirmation in **Authentication -> Sign In / Providers -> Email** so newly signed-up users can log in immediately.

Use the publishable/anon public key, NOT the `service_role` or secret key. Elevated keys are not needed for this assignment and must not be committed or exposed.

### Quick Start (Docker Compose)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ehtisham5618/Task-CRUD-API.git
   cd Task-CRUD-API
   ```

2. **Create `.env` from the template**
   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```

3. **Add your own values to `.env`**
   ```env
   DATABASE_URL=postgres://postgres:YOUR_PASSWORD@localhost:5432/tasks
   POSTGRES_PASSWORD=YOUR_PASSWORD
   POSTGRES_DB=tasks
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_or_publishable_key
   ```

4. **Start the stack**
   ```bash
   docker compose up
   ```

5. **Open the API**
   - API Base URL: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

6. **Stop the stack**
   ```bash
   docker compose down
   ```

Supabase runs externally, so no Supabase service is added to `docker-compose.yaml`.

### Manual Setup (Without Docker)

1. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `.env`**
   ```bash
   cp .env.example .env
   ```

   Set `DATABASE_URL`, `SUPABASE_URL`, and `SUPABASE_KEY` for your local environment.

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables

The committed `.env.example` file documents the required variables:

```env
DATABASE_URL=postgres://postgres:YOUR_PASSWORD@localhost:5432/tasks
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_DB=tasks
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_publishable_key
```

Security notes:
- `.env` is Git-ignored and must contain real local secrets only.
- `.env.example` is committed with placeholders only.
- `SUPABASE_KEY` must be the publishable or legacy anon public key.
- Do not use or commit the Supabase `service_role` or secret key.
- Do not commit access tokens, refresh tokens, passwords, or Authorization headers.

## Example cURL Output

Safe public route example:

```bash
$ curl -i http://localhost:8000/public/info
HTTP/1.1 200 OK
date: Tue, 01 Sep 2026 14:00:00 GMT
server: uvicorn
content-length: 54
content-type: application/json

{"message":"Welcome stranger! This info is public."}
```

Protected route without a token:

```bash
$ curl -i http://localhost:8000/protected/profile
HTTP/1.1 401 Unauthorized
date: Tue, 01 Sep 2026 14:00:00 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"error":"Access token required"}
```

## Testing Authentication

### Signup

```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"<password>"}'
```

Expected response: `201 Created`

### Login

```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"<password>"}'
```

Expected response: `200 OK` with `access_token` and `refresh_token`.

### Protected Profile

```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```

Expected response: `200 OK` with safe user metadata.

### Protected Dashboard

```bash
curl -i http://localhost:8000/protected/dashboard \
  -H "Authorization: Bearer <access_token>"
```

Expected response: `200 OK`. This route uses the same auth dependency as `/protected/profile`.

### Logout

```bash
curl -i -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <access_token>"
```

Expected response: `204 No Content` with an empty body.

## Swagger UI

Swagger UI is available at:

```text
http://localhost:8000/docs
```

Use the **Authorize** button to enter a bearer access token from `/auth/login`. Protected routes show bearer-auth locks:

- `GET /protected/profile`
- `GET /protected/dashboard`
- `POST /auth/logout`

Public routes do not require bearer authentication.

![Swagger UI with Bearer Authentication](docs/swagger-auth.png)

## PostgreSQL Verification

With the stack running, you can connect directly to PostgreSQL:

```bash
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

Example output:

```text
 id |       title       | done
----+-------------------+------
  1 | Learn FastAPI     | f
  2 | Build a CRUD API  | f
  3 | Deploy to GitHub  | f
```

## Project Structure

```text
Task-CRUD-API/
|-- main.py                  # FastAPI application with CRUD + auth endpoints
|-- database.py              # PostgreSQL connection management
|-- auth.py                  # Supabase client initialization
|-- Dockerfile               # Docker image definition for API container
|-- docker-compose.yaml      # API + PostgreSQL orchestration
|-- requirements.txt         # Python dependencies
|-- .env.example             # Environment variables template
|-- .gitignore               # Git ignore rules
|-- README.md                # Project documentation
|-- docs/
|   |-- swagger-ui.png       # Swagger UI screenshot from A3
|   `-- swagger-auth.png     # Swagger UI bearer auth screenshot from A4
`-- scraper/                 # Assignment 5 — Polite Scraper
    |-- src/
    |   `-- main.py          # Scraping pipeline
    |-- output/
    |   |-- books.json       # 60 validated book records
    |   |-- errors.json      # Validation failures
    |   `-- run-report.json  # Run metrics
    |-- requirements.txt     # Scraper dependencies
    |-- .gitignore           # Ignores cache/ and .venv/
    `-- README.md            # Scraper documentation
```

## Key Files

**`main.py`**
- Preserves the original CRUD routes
- Adds signup, login, logout, public info, profile, and dashboard routes
- Defines the reusable HTTPBearer auth dependency
- Verifies protected route tokens through Supabase

**`auth.py`**
- Initializes the Supabase client from environment variables
- Requires `SUPABASE_URL` and `SUPABASE_KEY`
- Does not hardcode or log secrets

**`database.py`**
- Opens PostgreSQL connections from `DATABASE_URL`
- Creates the `tasks` table when the app starts
- Seeds initial tasks only when the table is empty

**`docker-compose.yaml`**
- Runs PostgreSQL and the FastAPI API service
- Passes Supabase environment variables into the API container
- Keeps Supabase as an external hosted service

**`.env.example`**
- Documents required database and Supabase variables
- Uses placeholders only

## Database (PostgreSQL)

The API uses PostgreSQL running in Docker. On startup:

1. PostgreSQL starts in the `db` container.
2. FastAPI waits for the database health check.
3. `database.py` creates the `tasks` table if needed.
4. Three seed tasks are inserted only when the table is empty.
5. Data persists in the `taskdata` Docker volume.

All SQL queries use parameterized placeholders through `psycopg` to avoid SQL injection.

## Author

**Ehtisham Abid**

---

**Happy coding!**
