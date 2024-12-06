import mysql.connector
from mysql.connector import Error

def connect_db():
    """
    Establishes a connection to the 'prodev' database.
    Returns the connection object if successful, otherwise None.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",       
            user="silas",   
            password="1234", 
            database="prodev"        
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None

def stream_users_in_batches(batch_size):
    """
    Fetches rows of users from the database in batches using a generator.
    Yields batches of users.
    """
    connection = connect_db()
    if not connection:
        return
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")  
    
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # Yield a batch of users

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users to filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        for user in filtered_users:
            print(f"User: {user['name']}, Age: {user['age']}")
