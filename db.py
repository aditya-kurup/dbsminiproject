import sqlite3

DATABASE_PATH = 'flights.db'

def get_db_connection():
    """
    Create a database connection and return it
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
