from db import get_db_connection
from flight import get_flight_by_id, update_flight_seats

def create_booking(user_id, flight_id, passengers_count, passenger_details):
    """
    Create a new booking with passenger details
    Returns booking ID if successful, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        flight = get_flight_by_id(flight_id)
        if not flight or flight['available_seats'] < passengers_count:
            conn.close()
            return None
        
        total_price = flight['price'] * passengers_count
        
        if not update_flight_seats(flight_id, passengers_count):
            conn.close()
            return None
        
        cursor.execute(
            "INSERT INTO bookings (user_id, flight_id, total_passengers, total_price) VALUES (?, ?, ?, ?)",
            (user_id, flight_id, passengers_count, total_price)
        )
        booking_id = cursor.lastrowid
        
        for passenger in passenger_details:
            cursor.execute(
                """
                INSERT INTO passengers 
                (booking_id, first_name, last_name, date_of_birth, passport_number, phone_number)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (booking_id, passenger['first_name'], passenger['last_name'], 
                 passenger.get('date_of_birth'), passenger.get('passport_number'), 
                 passenger.get('phone_number'))
            )
            
        conn.commit()
        return booking_id
        
    except Exception as e:
        print(f"Error creating booking: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_user_bookings(user_id):
    """
    Get all bookings for a specific user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT b.*, f.flight_number, f.origin, f.destination, f.departure_time
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.user_id = ?
        ORDER BY b.booking_date DESC
        """,
        (user_id,)
    )
    
    bookings = [dict(booking) for booking in cursor.fetchall()]
    conn.close()
    
    return bookings

def get_booking_details(booking_id):
    """
    Get detailed information about a booking, including passengers
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT b.*, f.flight_number, f.origin, f.destination, 
        f.departure_time, f.arrival_time, f.price
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE b.id = ?
        """,
        (booking_id,)
    )
    
    booking = cursor.fetchone()
    if not booking:
        conn.close()
        return None
    
    cursor.execute(
        "SELECT * FROM passengers WHERE booking_id = ?",
        (booking_id,)
    )
    
    passengers = [dict(passenger) for passenger in cursor.fetchall()]
    conn.close()
    
    return {
        'booking': dict(booking),
        'passengers': passengers
    }
