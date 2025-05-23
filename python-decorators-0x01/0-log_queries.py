import sqlite3
import functools
import logging

# Configure logging to output queries with a simple format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - Query: %(message)s'
)

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the SQL query (first argument or keyword 'query')
        query = args[0] if args else kwargs.get('query', '')
        logging.info(query)
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")