
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',         # Replace with your MySQL username
            password='your_mysql_password'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',         
            password='your_mysql_password', 
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(200) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table 'user_data' created successfully.")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from a CSV file into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                # Generate a UUID for user_id
                user_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (user_id, row[0], row[1], row[2])
                )
        connection.commit()
        print("Data inserted successfully.")
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")




