import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle opening and closing database connections."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the database connection
        conn = sqlite3.connect('users.db')
        
        try:
            # Pass the connection to the original function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after the function execution
            conn.close()

    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function if it raises an exception."""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Try to call the function
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    # If an error occurs, retry after a delay
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    if attempt == retries:
                        # If max retries are reached, raise the exception
                        print("Max retries reached. Operation failed.")
                        raise e

        return wrapper

    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch users from the users table with retry mechanism."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users: {e}")

