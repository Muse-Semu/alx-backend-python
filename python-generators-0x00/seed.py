import mysql.connector
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@1234",  
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # Generate UUID if not provided in CSV
                user_id = str(uuid.uuid4()) if len(row) < 4 or not row[0] else row[0]
                name = row[1] if len(row) > 1 else ""
                email = row[2] if len(row) > 2 else ""
                age = float(row[3]) if len(row) > 3 and row[3] else 0.0
                
                insert_query = """
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def stream_rows(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
        return