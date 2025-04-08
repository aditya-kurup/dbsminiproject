// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for dynamic passenger form
    const passengerCountField = document.getElementById('passengers_count');
    if (passengerCountField) {
        passengerCountField.addEventListener('change', function() {
            if (typeof updatePassengerForms === 'function') {
                updatePassengerForms();
            } else {
                console.warn('updatePassengerForms function not found');
            }
        });
        
        // Try to initialize passenger forms if the function exists in the page scope
        if (typeof updatePassengerForms === 'function') {
            updatePassengerForms();
        }
    }
    
    // Flight search form validation
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', validateSearchForm);
    }
    
    // Initialize datepickers for any date field
    initializeDatepickers();
    
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 1s ease-out';
            message.style.opacity = 0;
            setTimeout(() => {
                message.remove();
            }, 1000);
        }, 5000);
    });
});

// Validate search form before submission
function validateSearchForm(event) {
    const origin = document.getElementById('origin').value;
    const destination = document.getElementById('destination').value;
    
    if (!origin && !destination) {
        event.preventDefault();
        alert('Please provide at least origin or destination for search.');
    }
}

// Initialize datepickers on date fields
function initializeDatepickers() {
    const dateFields = document.querySelectorAll('input[type="date"]');
    
    // Set min date for search date to today
    const searchDateField = document.getElementById('date');
    if (searchDateField) {
        const today = new Date().toISOString().split('T')[0];
        searchDateField.min = today;
    }
}

// Update total price based on passenger count
function updateTotalPrice() {
    const passengerCount = document.getElementById('passengers_count')?.value;
    const basePrice = document.getElementById('base_price')?.value;
    const totalPriceElement = document.getElementById('total_price');
    
    if (basePrice && totalPriceElement && passengerCount) {
        const price = parseFloat(basePrice);
        const totalPrice = price * parseInt(passengerCount);
        totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
    }
}

// Default implementation of updatePassengerForms
// This may be overridden in specific pages
function updatePassengerForms() {
    const passengerCount = document.getElementById('passengers_count')?.value || 1;
    const passengerForms = document.getElementById('passenger-forms');
    
    if (!passengerForms) return;
    
    // Clear current forms
    passengerForms.innerHTML = '';
    
    // Create forms for each passenger
    for (let i = 1; i <= passengerCount; i++) {
        passengerForms.innerHTML += `
            <div class="card mb-3">
                <div class="card-header">
                    <h3>Passenger ${i}</h3>
                </div>
                <div class="card-body">
                    <div class="form-group mb-3">
                        <label for="first_name_${i}" class="form-label">First Name*</label>
                        <input type="text" class="form-control" id="first_name_${i}" name="first_name_${i}" required>
                    </div>
                    <div class="form-group mb-3">
                        <label for="last_name_${i}" class="form-label">Last Name*</label>
                        <input type="text" class="form-control" id="last_name_${i}" name="last_name_${i}" required>
                    </div>
                    <div class="form-group mb-3">
                        <label for="dob_${i}" class="form-label">Date of Birth</label>
                        <input type="date" class="form-control datepicker" id="dob_${i}" name="dob_${i}">
                    </div>
                    <div class="form-group mb-3">
                        <label for="passport_${i}" class="form-label">Passport Number</label>
                        <input type="text" class="form-control" id="passport_${i}" name="passport_${i}">
                    </div>
                    <div class="form-group mb-3">
                        <label for="phone_${i}" class="form-label">Phone Number</label>
                        <input type="tel" class="form-control" id="phone_${i}" name="phone_${i}">
                    </div>
                </div>
            </div>
        `;
    }
    
    // Re-initialize datepickers for newly created forms
    initializeDatepickers();
    
    // Update total price
    updateTotalPrice();
}

// Live search for flights using AJAX
function liveSearch() {
    const origin = document.getElementById('origin')?.value || '';
    const destination = document.getElementById('destination')?.value || '';
    const date = document.getElementById('date')?.value || '';
    const resultsContainer = document.getElementById('search-results');
    
    if (!resultsContainer) return;
    
    if (!origin && !destination && !date) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    // Show loading indicator
    resultsContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Searching flights...</p></div>';
    
    // Make AJAX request to the server
    fetch(`/api/flights?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&date=${encodeURIComponent(date)}`)
        .then(response => response.json())
        .then(flights => {
            // Clear previous results
            resultsContainer.innerHTML = '';
            
            if (flights.length === 0) {
                resultsContainer.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle me-2"></i>No flights found matching your criteria.</div>';
                return;
            }
            
            resultsContainer.innerHTML = `<h2 class="mb-4"><i class="fas fa-plane me-2"></i>${flights.length} flights found</h2>`;
            const flightContainer = document.createElement('div');
            flightContainer.className = 'flight-cards';
            
            // Display each flight
            flights.forEach(flight => {
                const departureDate = new Date(flight.departure_time).toLocaleString();
                const arrivalDate = new Date(flight.arrival_time).toLocaleString();
                
                const flightCard = document.createElement('div');
                flightCard.className = 'flight-card';
                flightCard.innerHTML = `
                    <div class="flight-card-header">
                        <h3><i class="fas fa-plane me-2"></i>${flight.flight_number}</h3>
                        <span><i class="fas fa-chair me-1"></i> ${flight.available_seats} seats</span>
                    </div>
                    <div class="flight-card-body">
                        <div class="flight-info">
                            <p><i class="fas fa-plane-departure me-2"></i><strong>From:</strong> ${flight.origin}</p>
                            <p><i class="fas fa-plane-arrival me-2"></i><strong>To:</strong> ${flight.destination}</p>
                            <p><i class="far fa-clock me-2"></i><strong>Departure:</strong> ${departureDate}</p>
                            <p><i class="fas fa-clock me-2"></i><strong>Arrival:</strong> ${arrivalDate}</p>
                        </div>
                        <div class="flight-price">$${flight.price}</div>
                    </div>
                    <div class="flight-card-footer">
                        <a href="/flight/${flight.id}" class="btn btn-primary">
                            <i class="fas fa-info-circle me-2"></i>View Details
                        </a>
                    </div>
                `;
                
                flightContainer.appendChild(flightCard);
            });
            
            resultsContainer.appendChild(flightContainer);
        })
        .catch(error => {
            console.error('Error fetching flights:', error);
            resultsContainer.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>An error occurred while searching for flights.</div>';
        });
}
