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
