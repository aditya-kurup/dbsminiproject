import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

def register_user(username, password):
    """
    Register a new user in the database
    Returns True if successful, False if the username already exists
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    
    # Create new user
    hashed_password = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()
    return True

def authenticate_user(username, password):
    """
    Authenticate a user
    Returns user info if credentials are correct, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return {
            'id': user['id'],
            'username': user['username']
        }
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user['id'],
            'username': user['username']
        }
    return None
