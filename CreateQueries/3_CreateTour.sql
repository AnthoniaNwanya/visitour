CREATE TABLE IF NOT EXISTS tours (
    id SERIAL PRIMARY KEY,
    agency_id INTEGER REFERENCES agencies(id),
    tour_name VARCHAR(255) NOT NULL,
    description TEXT,
    country TEXT[] NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL NOT NULL,
    available_slots INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ALTER TABLE tours
-- ADD CONSTRAINT unique_agency_tour_name
-- UNIQUE (agency_id, tour_name);

-- ALTER TABLE tours
-- RENAME COLUMN country TO country;

-- DROP TABLE IF EXISTS agencies CASCADE;