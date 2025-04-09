from db import get_db_connection
from datetime import datetime

def search_flights(origin=None, destination=None, date=None):
    """
    Search for flights based on criteria
    Returns list of flights matching the search parameters
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM flights WHERE 1=1"
    params = []
    
    if origin:
        query += " AND origin LIKE ?"
        params.append(f"%{origin}%")
    
    if destination:
        query += " AND destination LIKE ?"
        params.append(f"%{destination}%")
    
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            start_date = date_obj.strftime("%Y-%m-%d 00:00:00")
            end_date = date_obj.strftime("%Y-%m-%d 23:59:59")
            query += " AND departure_time BETWEEN ? AND ?"
            params.append(start_date)
            params.append(end_date)
        except ValueError:
            print(f"Invalid date format: {date}")
    
    query += " AND available_seats > 0"
    query += " ORDER BY departure_time ASC"
    
    cursor.execute(query, params)
    flights = [dict(flight) for flight in cursor.fetchall()]
    conn.close()
    
    return flights

def get_flight_by_id(flight_id):
    """
    Get detailed information about a specific flight
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM flights WHERE id = ?", (flight_id,))
    flight = cursor.fetchone()
    conn.close()
    
    if flight:
        return dict(flight)
    return None

def update_flight_seats(flight_id, seats_to_book):
    """
    Update available seats when a booking is made
    Returns True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT available_seats FROM flights WHERE id = ?", (flight_id,))
        flight = cursor.fetchone()
        
        if not flight or flight['available_seats'] < seats_to_book:
            conn.close()
            return False
        
        new_seats = flight['available_seats'] - seats_to_book
        cursor.execute(
            "UPDATE flights SET available_seats = ? WHERE id = ?",
            (new_seats, flight_id)
        )
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error updating flight seats: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_flights(limit=None):
    """
    Get all available flights, with optional limit
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM flights WHERE available_seats > 0 ORDER BY departure_time ASC"
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    flights = [dict(flight) for flight in cursor.fetchall()]
    conn.close()
    
    return flights
