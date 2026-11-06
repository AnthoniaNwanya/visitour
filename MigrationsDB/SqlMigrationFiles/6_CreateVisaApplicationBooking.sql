CREATE TABLE IF NOT EXISTS visa_bookings (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    visa_id INTEGER NOT NULL REFERENCES visa_applications(id),
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    visa_name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    processing_fee NUMERIC(12, 2) NOT NULL CHECK (processing_fee >= 0),
    total_amount NUMERIC(12, 2)
        GENERATED ALWAYS AS (quantity * processing_fee) STORED,
    status VARCHAR(25) NOT NULL DEFAULT 'documents_required'
        CHECK (
            status IN (
                'documents_required',
                'submitted',
                'in_review',
                'approved',
                'rejected',
                'cancelled'
            )
        ),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_visa_bookings_agency_created
ON visa_bookings (agency_id, created_at DESC);
