CREATE TABLE IF NOT EXISTS tour_bookings (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    tour_id INTEGER NOT NULL REFERENCES tours(id),
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    tour_name VARCHAR(150) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount NUMERIC(12, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,
    status VARCHAR(25) NOT NULL DEFAULT 'pending_confirmation'
        CHECK (
            status IN (
                'pending_confirmation',
                'confirmed',
                'in_progress',
                'completed',
                'cancelled'
            )
        ),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tour_bookings_agency_created
ON tour_bookings (agency_id, created_at DESC);
