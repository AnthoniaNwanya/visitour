CREATE TABLE IF NOT EXISTS carts (
    id SERIAL PRIMARY KEY,
    traveler_id INTEGER NOT NULL REFERENCES travelers(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (
            status IN ('active', 'pending_payment', 'checked_out', 'abandoned')
        ),
    total_order_summary NUMERIC(12, 2) NOT NULL DEFAULT 0        CHECK (total_order_summary >= 0),
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

