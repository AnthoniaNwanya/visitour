CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE SET NULL,
    payment_reference VARCHAR(255) UNIQUE NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'NGN',
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'paid', 'failed', 'cancelled')),
    payment_method VARCHAR(50) NOT NULL DEFAULT 'manual',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE payments
ADD COLUMN IF NOT EXISTS cart_id INTEGER REFERENCES carts(id) ON DELETE SET NULL;

ALTER TABLE payments
ALTER COLUMN amount TYPE NUMERIC(12, 2)
USING amount::NUMERIC(12, 2);

CREATE UNIQUE INDEX IF NOT EXISTS uq_pending_payment_cart
ON payments (cart_id)
WHERE cart_id IS NOT NULL AND status = 'pending';

CREATE INDEX IF NOT EXISTS idx_payments_cart_created
ON payments (cart_id, created_at DESC);
