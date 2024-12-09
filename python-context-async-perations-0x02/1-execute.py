iimport mysql.connector
from mysql.connector import Error

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """
        Initialize the context manager with database name, query, and parameters.
        """
        self.db_name = db_name
        self.query = query
        self.params = params or []
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        """
        Open the connection and prepare to execute the query.
i        """
        try:
            print("Connecting to the MySQL database...")
            self.connection = mysql.connector.connect(
                host="localhost",    
                database=self.db_name,
                user="silas",    
                password="2480"  
            )
            self.cursor = self.connection.cursor()
            return self  # Return the instance to access results after execution
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def execute(self):
        """
        Execute the query and store the result.
        """
        try:
            print(f"Executing query: {self.query} with parameters: {self.params}")
            self.cursor.execute(self.query, self.params)
            self.result = self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the cursor and connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            print("Closing the MySQL connection...")
            self.connection.close()
        if exc_type:
            print(f"An exception occurred: {exc_value}")

# Example Usage: Create a database, insert data, and query it
def setup_database():
    with ExecuteQuery("test_db", """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
    """) as db:
        db.execute()
    
    with ExecuteQuery("test_db", """
        INSERT INTO users (name, age) VALUES (%s, %s)
    """, params=("Alice", 30)) as db:
        db.execute()

    with ExecuteQuery("test_db", """
        INSERT INTO users (name, age) VALUES (%s, %s)
    """, params=("Bob", 20)) as db:
        db.execute()

def query_users():
    query = "SELECT * FROM users WHERE age > %s"
    param = (25,)
    with ExecuteQuery("test_db", query, param) as db:
        db.execute()
        print("Query Results:", db.result)

# Run Setup and Query
setup_database()
query_users()

