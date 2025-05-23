# Python Database Row Streaming Generator

## Overview
This project provides a Python script (`seed.py`) that sets up a MySQL database named `ALX_prodev`, creates a `user_data` table, populates it with data from a CSV file, and includes a generator function to stream rows one by one from the table. The script is designed to work with the provided `0-main.py` for testing.

## Prerequisites
- Python 3.6 or higher
- MySQL Server installed and running
- `mysql-connector-python` library
- A CSV file named `user_data.csv` with columns: `user_id` (optional), `name`, `email`, `age`

## Installation
1. Install the required Python package:
   ```bash
   pip install mysql-connector-python
   ```

2. Ensure MySQL is running on your system. Update the MySQL credentials (host, user, password) in `seed.py` if necessary:
   ```python
   connection = mysql.connector.connect(
       host="localhost",
       user="root",
       password=""  # Update with your MySQL password
   )
   ```

3. Place the `user_data.csv` file in the same directory as `seed.py`. The CSV should have the following format (header row optional):
   ```
   user_id,name,email,age
   00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
   ...
   ```

## Project Structure
- `seed.py`: Main script containing database setup and generator functions
- `0-main.py`: Test script to verify database creation and data insertion
- `user_data.csv`: Sample data file for populating the database
- `README.md`: This file

## Functions in `seed.py`
- `connect_db()`: Connects to the MySQL server.
- `create_database()`: Creates the `ALX_prodev` database if it doesn't exist.
- `connect_to_prodev()`: Connects to the `ALX_prodev` database.
- `create_table()`: Creates the `user_data` table with fields:
  - `user_id` (VARCHAR(36), Primary Key, Indexed)
  - `name` (VARCHAR(255), NOT NULL)
  - `email` (VARCHAR(255), NOT NULL)
  - `age` (DECIMAL(5,2), NOT NULL)
- `insert_data()`: Inserts data from `user_data.csv` into the `user_data` table, generating UUIDs for missing `user_id` values.
- `stream_rows()`: Generator function that yields rows from `user_data` one by one.

## Usage
1. Run the test script to set up the database and verify functionality:
   ```bash
   ./0-main.py
   ```
   Expected output:
   ```
   connection successful
   Table user_data created successfully
   Database ALX_prodev is present
   [(...)]  # Sample rows from user_data
   ```

2. Use the generator to stream rows in your own script:
   ```python
   import seed

   connection = seed.connect_to_prodev()
   if connection:
       for row in seed.stream_rows(connection):
           print(row)  # Process each row
       connection.close()
   ```

## Notes
- The `stream_rows()` generator is memory-efficient, fetching one row at a time.
- The `insert_data()` function uses `INSERT IGNORE` to avoid duplicate entries.
- Ensure the MySQL server is running and accessible before executing the script.
- Update the MySQL password in `seed.py` to match your configuration.
- The CSV file should be properly formatted to avoid data insertion errors.

## Troubleshooting
- **MySQL connection errors**: Verify MySQL is running and credentials are correct.
- **CSV file errors**: Ensure `user_data.csv` exists and follows the expected format.
- **Module