#!/usr/bin/env python3
"""
Module: 0-databaseconnection
Defines a custom context manager for managing database connections.
"""

import sqlite3

class DatabaseConnection:
    """Context manager for handling database connections."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit changes and close the connection."""
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
            self.conn.close()


# === Usage Example ===
if __name__ == "__main__":
    db_name = "example.db"

    # Ensure table exists for demonstration
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """)
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))

    # Use the context manager to perform SELECT query
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Users:")
        for row in rows:
            print(row)
