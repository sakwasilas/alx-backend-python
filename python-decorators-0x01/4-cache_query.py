import time
import sqlite3
import functools

# Dictionary to store the cached results based on query strings
query_cache = {}

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

def cache_query(func):
    """Decorator to cache query results based on the query string."""
    
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already in cache
        if query in query_cache:
            print("Using cached result...")
            return query_cache[query]
        
        # If not cached, call the function to get the result
        result = func(conn, query, *args, **kwargs)
        
        # Cache the result with the query string as the key
        query_cache[query] = result
        print("Query result cached.")
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from the users table and cache the result."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

