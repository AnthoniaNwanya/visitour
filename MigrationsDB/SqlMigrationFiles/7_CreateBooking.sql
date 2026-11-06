CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    traveler_id INTEGER NOT NULL REFERENCES travelers(id),
    cart_id INTEGER REFERENCES carts(id) ON DELETE SET NULL,
    booking_reference VARCHAR(50) NOT NULL UNIQUE,
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'NGN',
    status VARCHAR(20) NOT NULL DEFAULT 'pending_payment'
        CHECK (status IN ('pending_payment', 'booked', 'cancelled')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
