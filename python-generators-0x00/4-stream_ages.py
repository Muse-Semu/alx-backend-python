import mysql.connector

def stream_user_ages():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",  
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        
        # Fetch ages one by one
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield float(row[0])  # Convert DECIMAL to float
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    calculate_average_age()