CREATE TABLE visa_bookings (
    id SERIAL PRIMARY KEY,
    visa_id INTEGER REFERENCES visa_applications(id),
    booking_id INTEGER REFERENCES bookings(id)
);



