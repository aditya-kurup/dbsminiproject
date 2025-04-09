import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DATABASE_PATH = 'flights.db'

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
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
    
    admin_password_hash = generate_password_hash('admin')
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ('admin', admin_password_hash)
    )
    
    # Hardcoded flights instead of random generation
    now = datetime.now()
    
    # 5 flights from New York to London
    flights = [
        # New York to London flights
        {
            'flight_number': 'BA178',
            'origin': 'New York',
            'destination': 'London',
            'departure_time': (now + timedelta(days=3)).replace(hour=21, minute=30, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=4)).replace(hour=9, minute=30, second=0, microsecond=0),
            'price': 799.99,
            'total_seats': 250,
            'available_seats': 180
        },
        {
            'flight_number': 'VS4',
            'origin': 'New York',
            'destination': 'London',
            'departure_time': (now + timedelta(days=4)).replace(hour=18, minute=0, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=5)).replace(hour=6, minute=0, second=0, microsecond=0),
            'price': 849.50,
            'total_seats': 280,
            'available_seats': 220
        },
        {
            'flight_number': 'AA100',
            'origin': 'New York',
            'destination': 'London',
            'departure_time': (now + timedelta(days=5)).replace(hour=19, minute=45, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=6)).replace(hour=7, minute=55, second=0, microsecond=0),
            'price': 705.75,
            'total_seats': 200,
            'available_seats': 145
        },
        {
            'flight_number': 'UA923',
            'origin': 'New York',
            'destination': 'London',
            'departure_time': (now + timedelta(days=7)).replace(hour=20, minute=15, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=8)).replace(hour=8, minute=30, second=0, microsecond=0),
            'price': 750.00,
            'total_seats': 220,
            'available_seats': 190
        },
        {
            'flight_number': 'DL2',
            'origin': 'New York',
            'destination': 'London',
            'departure_time': (now + timedelta(days=10)).replace(hour=22, minute=0, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=11)).replace(hour=10, minute=15, second=0, microsecond=0),
            'price': 899.99,
            'total_seats': 300,
            'available_seats': 260
        },
        
        # London to New York flights
        {
            'flight_number': 'BA177',
            'origin': 'London',
            'destination': 'New York',
            'departure_time': (now + timedelta(days=4)).replace(hour=11, minute=0, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=4)).replace(hour=14, minute=0, second=0, microsecond=0),
            'price': 819.99,
            'total_seats': 250,
            'available_seats': 170
        },
        {
            'flight_number': 'VS45',
            'origin': 'London',
            'destination': 'New York',
            'departure_time': (now + timedelta(days=6)).replace(hour=10, minute=30, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=6)).replace(hour=13, minute=30, second=0, microsecond=0),
            'price': 879.50,
            'total_seats': 280,
            'available_seats': 200
        },
        
        # Other popular routes
        {
            'flight_number': 'LH400',
            'origin': 'New York',
            'destination': 'Berlin',
            'departure_time': (now + timedelta(days=5)).replace(hour=16, minute=30, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=6)).replace(hour=6, minute=45, second=0, microsecond=0),
            'price': 745.00,
            'total_seats': 200,
            'available_seats': 140
        },
        {
            'flight_number': 'AF1180',
            'origin': 'Paris',
            'destination': 'New York',
            'departure_time': (now + timedelta(days=7)).replace(hour=10, minute=15, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=7)).replace(hour=12, minute=45, second=0, microsecond=0),
            'price': 840.50,
            'total_seats': 220,
            'available_seats': 170
        },
        {
            'flight_number': 'EK201',
            'origin': 'Dubai',
            'destination': 'New York',
            'departure_time': (now + timedelta(days=8)).replace(hour=8, minute=30, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=8)).replace(hour=14, minute=15, second=0, microsecond=0),
            'price': 1250.00,
            'total_seats': 350,
            'available_seats': 280
        },
        {
            'flight_number': 'SQ21',
            'origin': 'Singapore',
            'destination': 'Tokyo',
            'departure_time': (now + timedelta(days=3)).replace(hour=9, minute=45, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=3)).replace(hour=17, minute=30, second=0, microsecond=0),
            'price': 680.25,
            'total_seats': 240,
            'available_seats': 190
        },
        {
            'flight_number': 'QF9',
            'origin': 'Sydney',
            'destination': 'London',
            'departure_time': (now + timedelta(days=10)).replace(hour=18, minute=0, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=11)).replace(hour=20, minute=45, second=0, microsecond=0),
            'price': 1750.50,
            'total_seats': 280,
            'available_seats': 230
        },
        {
            'flight_number': 'JL5',
            'origin': 'Tokyo',
            'destination': 'Paris',
            'departure_time': (now + timedelta(days=6)).replace(hour=12, minute=30, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=6)).replace(hour=18, minute=45, second=0, microsecond=0),
            'price': 950.75,
            'total_seats': 260,
            'available_seats': 210
        },
        {
            'flight_number': 'EY101',
            'origin': 'Abu Dhabi',
            'destination': 'New York',
            'departure_time': (now + timedelta(days=9)).replace(hour=9, minute=0, second=0, microsecond=0),
            'arrival_time': (now + timedelta(days=9)).replace(hour=15, minute=15, second=0, microsecond=0),
            'price': 1150.00,
            'total_seats': 300,
            'available_seats': 265
        }
    ]
    
    for flight in flights:
        cursor.execute('''
        INSERT INTO flights 
        (flight_number, origin, destination, departure_time, arrival_time, price, total_seats, available_seats)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            flight['flight_number'], 
            flight['origin'], 
            flight['destination'], 
            flight['departure_time'], 
            flight['arrival_time'], 
            flight['price'], 
            flight['total_seats'], 
            flight['available_seats']
        ))
    
    conn.commit()
    conn.close()
    
    print("Database initialized")

if __name__ == "__main__":
    init_db()
