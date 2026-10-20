CREATE TABLE IF NOT EXISTS visa_applications (
    id SERIAL PRIMARY KEY,
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    visa_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    visa_type_id INTEGER NOT NULL REFERENCES visa_types(id),
    processing_time_value INTEGER NOT NULL,
    processing_time_unit VARCHAR(20) NOT NULL DEFAULT 'DAY',
    processing_fee DECIMAL(12, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DROP TABLE IF EXISTS visa_applications CASCADE;
