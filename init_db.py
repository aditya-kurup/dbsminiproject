import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Database setup
DATABASE_PATH = 'flights.db'

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
    DROP TABLE IF EXISTS passengers;
    DROP TABLE IF EXISTS bookings;
    DROP TABLE IF EXISTS flights;
    DROP TABLE IF EXISTS users;
    
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TIMESTAMP NOT NULL,
        arrival_time TIMESTAMP NOT NULL,
        price REAL NOT NULL,
        total_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL
    );
    
    CREATE TABLE bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_passengers INTEGER NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (flight_id) REFERENCES flights (id)
    );
    
    CREATE TABLE passengers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT,
        passport_number TEXT,
        phone_number TEXT,
        FOREIGN KEY (booking_id) REFERENCES bookings (id)
    );
    ''')
    
    # Insert sample admin user
    admin_password_hash = generate_password_hash('admin')
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ('admin', admin_password_hash)
    )
    
    # Insert sample flights
    cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Paris', 'Dubai', 'Mumbai', 'Singapore', 'Berlin', 'Rome']
    flight_prefixes = ['BA', 'AA', 'UA', 'LH', 'EK', 'QF', 'SQ', 'AF', 'DL', 'JL']
    
    for i in range(20):
        # Generate flight details
        origin_idx = random.randint(0, len(cities) - 1)
        dest_idx = random.randint(0, len(cities) - 1)
        while dest_idx == origin_idx:  # Make sure origin and destination are different
            dest_idx = random.randint(0, len(cities) - 1)
            
        origin = cities[origin_idx]
        destination = cities[dest_idx]
        flight_number = f"{flight_prefixes[random.randint(0, len(flight_prefixes) - 1)]}{random.randint(100, 999)}"
        
        # Generate random dates within the next month
        days_ahead = random.randint(1, 30)
        departure_date = (datetime.now() + timedelta(days=days_ahead)).replace(
            hour=random.randint(0, 23),
            minute=random.choice([0, 15, 30, 45]),
            second=0,  # Explicitly set seconds to 0
            microsecond=0  # Explicitly set microseconds to 0
        )
        
        # Flight duration between 1-15 hours
        flight_duration = timedelta(hours=random.randint(1, 15))
        arrival_date = departure_date + flight_duration
        
        price = round(random.uniform(100, 1500), 2)
        total_seats = random.choice([120, 150, 180, 200, 250])
        available_seats = total_seats - random.randint(0, total_seats // 2)  # Random number of seats already booked
        
        cursor.execute('''
        INSERT INTO flights 
        (flight_number, origin, destination, departure_time, arrival_time, price, total_seats, available_seats)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (flight_number, origin, destination, departure_date, arrival_date, price, total_seats, available_seats))
    
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db()
