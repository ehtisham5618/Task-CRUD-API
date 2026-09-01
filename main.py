from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from database import get_db_connection, init_db

app = FastAPI(title="Task API", version="1.0")

# Initialize database on startup
init_db()

# Custom exception handler for validation errors in POST/PUT
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid request body"}
    )

# Custom exception handler for HTTPException to return "error" field
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Task model
class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def title_valid(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v

# Root endpoint
@app.get("/")
def read_root():
    """Get API metadata and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """Check API health status."""
    return {"status": "ok"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    """Retrieve all tasks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, done FROM tasks")
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    
    tasks = []
    for row in rows:
        tasks.append(Task(
            id=row[0],
            title=row[1],
            done=row[2]
        ))
    return tasks

# Get a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Retrieve a task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    
    return Task(
        id=row[0],
        title=row[1],
        done=row[2]
    )

# Create a new task
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task: TaskCreate):
    """Create a new task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done",
            (task.title, False)
        )
        row = cursor.fetchone()
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    
    return Task(id=row[0], title=row[1], done=row[2])

# Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task by ID."""
    # Check if at least one field is provided
    if task_update.title is None and task_update.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title or done) must be provided"
        )
    
    # Validate title if provided
    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or whitespace"
        )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # First check if task exists
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        # Get current values
        current_title = row[1]
        current_done = row[2]
        
        # Update with provided values or keep existing
        new_title = task_update.title if task_update.title is not None else current_title
        new_done = task_update.done if task_update.done is not None else current_done
        
        # Update in database
        cursor.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
            (new_title, new_done, task_id)
        )
        updated_row = cursor.fetchone()
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    
    return Task(id=updated_row[0], title=updated_row[1], done=updated_row[2])

# Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if task exists
        cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        # Delete the task
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
