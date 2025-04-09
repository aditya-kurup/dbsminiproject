from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user import register_user, authenticate_user, get_user_by_id
from flight import search_flights, get_flight_by_id, get_all_flights
from booking import create_booking, get_user_bookings, get_booking_details
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

def login_required(view):
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return view(**kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

@app.route('/')
def index():
    upcoming_flights = get_all_flights(limit=6)
    return render_template('index.html', flights=upcoming_flights)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if register_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('You have been logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    bookings = get_user_bookings(session['user_id'])
    return render_template('dashboard.html', bookings=bookings)

@app.route('/flights')
def flights():
    all_flights = get_all_flights()
    return render_template('flights.html', flights=all_flights)

@app.route('/flight/<int:flight_id>')
def flight_details(flight_id):
    flight = get_flight_by_id(flight_id)
    if not flight:
        flash('Flight not found', 'danger')
        return redirect(url_for('flights'))
    
    return render_template('flight_details.html', flight=flight)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        date = request.form.get('date')
        
        flights = search_flights(origin, destination, date)
        search_params = {
            'origin': origin,
            'destination': destination,
            'date': date
        }
        
        return render_template('search_results.html', flights=flights, search_params=search_params)
    
    return render_template('search.html')

@app.route('/api/flights')
def api_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    
    flights = search_flights(origin, destination, date)
    return jsonify(flights)

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
@login_required
def book_flight(flight_id):
    flight = get_flight_by_id(flight_id)
    if not flight:
        flash('Flight not found', 'danger')
        return redirect(url_for('flights'))
    
    if request.method == 'POST':
        passengers_count = int(request.form.get('passengers_count', 1))
        
        passenger_details = []
        for i in range(1, passengers_count + 1):
            passenger = {
                'first_name': request.form.get(f'first_name_{i}'),
                'last_name': request.form.get(f'last_name_{i}'),
                'date_of_birth': request.form.get(f'dob_{i}'),
                'passport_number': request.form.get(f'passport_{i}'),
                'phone_number': request.form.get(f'phone_{i}')
            }
            passenger_details.append(passenger)
        
        booking_id = create_booking(session['user_id'], flight_id, passengers_count, passenger_details)
        if booking_id:
            flash('Booking successful!', 'success')
            return redirect(url_for('booking_confirmation', booking_id=booking_id))
        else:
            flash('Failed to create booking. Please try again.', 'danger')
    
    return render_template('book_flight.html', flight=flight)

@app.route('/booking/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    booking_info = get_booking_details(booking_id)
    if not booking_info or booking_info['booking']['user_id'] != session['user_id']:
        flash('Booking not found or access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('booking_confirmation.html', 
                          booking=booking_info['booking'], 
                          passengers=booking_info['passengers'])

@app.route('/booking_details/<int:booking_id>')
@login_required
def booking_details(booking_id):
    booking_info = get_booking_details(booking_id)
    if not booking_info or booking_info['booking']['user_id'] != session['user_id']:
        flash('Booking not found or access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('booking_details.html', 
                          booking=booking_info['booking'], 
                          passengers=booking_info['passengers'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.template_filter('date_format')
def date_format(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    
    if isinstance(value, str):
        try:
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M']:
                try:
                    value = datetime.strptime(value, fmt)
                    break
                except ValueError:
                    continue
        except Exception as e:
            print(f"Error parsing date: {e}")
            return value
    
    try:
        return value.strftime(format)
    except Exception as e:
        print(f"Error formatting date: {e}")
        return str(value)

@app.template_filter('datetime')
def parse_datetime(value):
    if value is None:
        return None
        
    if isinstance(value, str):
        try:
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M']:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            return value
        except Exception as e:
            print(f"Error parsing datetime: {e}")
            return value
    return value

if __name__ == '__main__':
    app.run(debug=True)
