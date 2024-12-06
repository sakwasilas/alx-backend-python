import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle opening and closing database connections."""
    
    @functools.wraps(func)  # Ensures that the decorated function retains its name and docstring
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

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)

