CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    traveler_id INTEGER REFERENCES travelers(id),  
    booking_reference VARCHAR(255) UNIQUE NOT NULL,
    booking_type VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending_payment',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


