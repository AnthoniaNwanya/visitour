Create table visa_applications (
    id SERIAL PRIMARY KEY,
    agency_id INTEGER REFERENCES agencies(id),
    destination VARCHAR(255) NOT NULL,
    visa_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'available',
    processing_fees INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

