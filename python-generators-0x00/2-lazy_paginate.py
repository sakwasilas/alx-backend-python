import mysql.connector

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='password',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def paginate_users(connection, page_size, offset):
    """
    Fetches a single page of users from the database starting at a specific offset.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except mysql.connector.Error as e:
        print(f"Error fetching paginated users: {e}")
        return []

def lazy_paginate(page_size):
    """
    A generator function that fetches users page by page from the database.
    Lazily loads each page and yields one user at a time.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        offset = 0
        while True:
            # Fetch the next page of data
            page = paginate_users(connection, page_size, offset)
            if not page:  # Stop when no more data is available
                break
            
            # Yield each user in the current page
            for user in page:
                yield user
            
            # Move to the next page
            offset += page_size
    finally:
        connection.close()

# Example usage
if __name__ == "__main__":
    page_size = 2  # Set the number of users per page
    for user in lazy_paginate(page_size):
        print(user)


