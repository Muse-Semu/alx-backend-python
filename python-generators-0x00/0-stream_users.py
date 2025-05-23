import mysql.connector

def stream_users():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        
        # Execute query to fetch all rows from user_data
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Fetch and yield each row as a dictionary
        for row in cursor:
            yield {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': int(row[3])  # Convert DECIMAL to int to match expected output
            }
        
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return