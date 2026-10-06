CREATE TABLE IF NOT EXISTS agencies (
    id SERIAL PRIMARY KEY,
    agency_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255) NOT NULL ,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING_VERIFICATION',
    cac_number VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ALTER TABLE agencies
-- ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255) NOT NULL;


-- ALTER TABLE agencies
-- ADD CONSTRAINT agency_name_unique UNIQUE (agency_name);


-- DROP TABLE IF EXISTS agencies CASCADE;


