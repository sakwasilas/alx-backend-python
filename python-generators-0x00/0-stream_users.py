import mysql.connector

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='silas',  
            password='1234',  
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def stream_users():
    """Generator function to fetch rows one by one from the user_data table using yield."""
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for better readability
        cursor.execute("SELECT * FROM user_data;")  # Query to fetch all rows
        for row in cursor:  # Single loop to iterate over query results
            yield row  # Yield each row one by one
    except mysql.connector.Error as e:
        print(f"Error fetching users: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Example usage of the stream_users generator
    for user in stream_users():
        print(user)


