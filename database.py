"""PostgreSQL database connection and initialization module."""
import os
import time
import psycopg
from psycopg import sql


def get_db_connection():
    """Get a PostgreSQL database connection."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Retry logic to handle container startup delays
    max_retries = 30
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            conn = psycopg.connect(database_url)
            return conn
        except psycopg.OperationalError as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise


def init_db():
    """Initialize the database with tasks table and seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        conn.commit()
        
        # Count existing tasks
        cursor.execute("SELECT COUNT(*) as count FROM tasks")
        count = cursor.fetchone()[0]
        
        # Seed initial tasks only if table is empty
        if count == 0:
            seed_tasks = [
                ("Learn FastAPI", False),
                ("Build a CRUD API", False),
                ("Deploy to GitHub", False),
            ]
            
            for title, done in seed_tasks:
                cursor.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    (title, done)
                )
            conn.commit()
    finally:
        cursor.close()
        conn.close()
