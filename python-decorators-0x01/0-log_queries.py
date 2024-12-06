import sqlite3
import functools
import logging

# Set up logging to print to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)  # Preserve the original function's name and docstring
    def wrapper(query, *args, **kwargs):
        # Log the SQL query before executing it
        logging.info(f"Executing query: {query}")
        
        # Call the original function to execute the query
        return func(query, *args, **kwargs)
    
    return wrapper

# Function to fetch all users from the database
@log_queries
def fetch_all_users(query):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# Example query to fetch users
users = fetch_all_users("SELECT * FROM users")

# Optionally, print the users to see the results
print(users)

