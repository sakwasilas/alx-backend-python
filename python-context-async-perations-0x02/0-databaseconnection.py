import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            # Establish the connection
            print("Connecting to the MySQL database...")
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connection successful.")
                self.cursor = self.connection.cursor()
                return self.cursor
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            print("Closing the database connection...")
            self.connection.close()

# Example: Using the context manager with MySQL
def query_database():
    # Replace these with your actual database credentials
    db_config = {
        "host": "localhost",
        "database": "your_database_name",
        "user": "your_username",
        "password": "your_password"
    }

    query = "SELECT * FROM users"

    with DatabaseConnection(**db_config) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)

# Setup and run
if __name__ == "__main__":
    query_database()
