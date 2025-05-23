import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        
        # Execute query to fetch all rows
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Fetch rows in batches
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield [{
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': int(row[3])  # Convert DECIMAL to int
            } for row in rows]
        
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def batch_processing(batch_size):
    # Process batches and filter users over 25
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user