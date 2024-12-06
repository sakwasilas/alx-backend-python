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

def transactional(func):
    """Decorator to handle database transactions."""
    
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Start a transaction
            conn.begin()
            
            # Call the original function
            result = func(conn, *args, **kwargs)
            
            # If no error occurred, commit the transaction
            conn.commit()
            return result
        
        except Exception as e:
            # If an error occurred, rollback the transaction
            conn.rollback()
            print(f"Error: {e}. Transaction rolled back.")
            raise  # Re-raise the error so it can be handled further up if needed

    return wrapper

@with_db_connection
@transactional
def insert_user(conn, user_id, name, email, age):
    """Inserts a new user into the users table."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)",
                   (user_id, name, email, age))
    return "User inserted successfully"

# Example usage:
try:
    # Attempt to insert a new user (replace with actual user details)
    result = insert_user(user_id=3, name='Charlie', email='charlie@example.com', age=30)
    print(result)
except Exception as e:
    print(f"Failed to insert user: {e}")

