import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
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

def stream_user_ages():
    """
    Generator that streams user ages one by one from the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for age in cursor:
            yield age[0]  # Yield the age value
        cursor.close()
    finally:
        connection.close()

def calculate_average_age():
    """
    Calculate the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")

# Run the script
if __name__ == "__main__":
    calculate_average_age()


