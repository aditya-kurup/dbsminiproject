# Flight Booking System

A database system for a flight booking application.

## Database Schema

The database consists of four main tables:
- `users`: Stores user account information
- `flights`: Stores flight details
- `bookings`: Records bookings made by users
- `passengers`: Stores passenger information for each booking

## Setup Instructions

1. Make sure you have Python installed (3.7+ recommended)
2. Install required packages:
```
pip install werkzeug
```

3. Initialize the database:
```
python init_db.py
```

4. Use the modules to interact with the database:
   - `user.py`: User management
   - `flight.py`: Flight search and management
   - `booking.py`: Booking creation and retrieval

## Default Admin User

Username: admin
Password: admin

## Example Usage

```python
# Search for flights
from flight import search_flights
flights = search_flights(origin="New York", destination="London")

# Create a user
from user import register_user
register_user("johndoe", "securepassword")

# Authenticate a user
from user import authenticate_user
user = authenticate_user("johndoe", "securepassword")

# Create a booking
from booking import create_booking
passenger_details = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'date_of_birth': '1990-01-01',
        'passport_number': 'AB123456',
        'phone_number': '+1234567890'
    }
]
booking_id = create_booking(user['id'], flight_id=1, passengers_count=1, passenger_details=passenger_details)
```
