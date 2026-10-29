CREATE TABLE IF NOT EXISTS carts (
    id SERIAL PRIMARY KEY,
    traveler_id INTEGER NOT NULL REFERENCES travelers(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (
            status IN ('active', 'pending_payment', 'checked_out', 'abandoned')
        ),
    total_order_summary NUMERIC(12, 2) NOT NULL DEFAULT 0
        CHECK (total_order_summary >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_traveler_active_cart
ON carts (traveler_id)
WHERE status = 'active';

ALTER TABLE carts DROP CONSTRAINT IF EXISTS carts_status_check;
ALTER TABLE carts DROP CONSTRAINT IF EXISTS ck_carts_status;
ALTER TABLE carts
ADD CONSTRAINT ck_carts_status
CHECK (status IN ('active', 'pending_payment', 'checked_out', 'abandoned'));

CREATE TABLE IF NOT EXISTS cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    booking_type VARCHAR(10) NOT NULL
        CHECK (booking_type IN ('tour', 'visa')),
    item_id INTEGER NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount NUMERIC(12, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cart_item UNIQUE (cart_id, booking_type, item_id)
);

CREATE OR REPLACE FUNCTION update_cart_total_order_summary()
RETURNS TRIGGER AS $$
DECLARE
    affected_cart_id INTEGER;
BEGIN
    IF TG_OP = 'DELETE' THEN
        affected_cart_id := OLD.cart_id;
    ELSE
        affected_cart_id := NEW.cart_id;
    END IF;

    UPDATE carts
    SET total_order_summary = COALESCE(
            (SELECT SUM(total_amount) FROM cart_items
             WHERE cart_id = affected_cart_id),
            0
        ),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = affected_cart_id;

    IF TG_OP = 'UPDATE' AND OLD.cart_id <> NEW.cart_id THEN
        UPDATE carts
        SET total_order_summary = COALESCE(
                (SELECT SUM(total_amount) FROM cart_items
                 WHERE cart_id = OLD.cart_id),
                0
            ),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = OLD.cart_id;

        DELETE FROM carts
        WHERE id = OLD.cart_id
          AND NOT EXISTS (
              SELECT 1 FROM cart_items WHERE cart_id = OLD.cart_id
          );
    END IF;

    IF TG_OP = 'DELETE' THEN
        DELETE FROM carts
        WHERE id = OLD.cart_id
          AND NOT EXISTS (
              SELECT 1 FROM cart_items WHERE cart_id = OLD.cart_id
          );
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_cart_total_order_summary ON cart_items;
CREATE TRIGGER trg_update_cart_total_order_summary
AFTER INSERT OR UPDATE OR DELETE ON cart_items
FOR EACH ROW
EXECUTE FUNCTION update_cart_total_order_summary();

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

CREATE INDEX IF NOT EXISTS idx_tour_bookings_agency_created
ON tour_bookings (agency_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_visa_bookings_agency_created
ON visa_bookings (agency_id, created_at DESC);
