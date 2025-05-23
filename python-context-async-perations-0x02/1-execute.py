
import sqlite3

class ExecuteQuery:
    """Context manager that executes a query and manages DB connection."""
    
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, return result."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# === Usage Example ===
if __name__ == "__main__":
    db_name = "example.db"

    # Ensure users table exists and has age data
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        cur.execute("DELETE FROM users")
        cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 22),
            ("Charlie", 28),
            ("David", 19)
        ])
        conn.commit()

    # Use ExecuteQuery to get users older than 25
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_name, query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)
