CREATE TABLE tour_bookings (
    id SERIAL PRIMARY KEY,
    tour_id INTEGER REFERENCES tours(id),
    booking_id INTEGER REFERENCES bookings(id)
);
