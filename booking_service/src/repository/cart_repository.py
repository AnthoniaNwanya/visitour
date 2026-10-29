from uuid import uuid4

from psycopg2.extras import DictCursor

from models.enums.booking_status import BookingStatus
from models.enums.booking_type import BookingType
from models.enums.cart_status import CartStatus
from repository.database.connection import get_db_connection
from services.exception.exceptions import (
    CartItemNotFoundError,
    CartItemUnavailableError,
    CartNotEditableError,
    CartNotFoundError,
    CartPriceChangedError,
    ItemNotFoundError,
)


class CartRepository:
    @staticmethod
    def _close(connection, cursor, rollback=False):
        if rollback:
            connection.rollback()
        if cursor is not None:
            cursor.close()
        connection.close()

    @staticmethod
    def _get_item(
        cursor, booking_type: BookingType, item_id: int, for_update: bool = False
    ):
        if booking_type == BookingType.TOUR:
            cursor.execute(
                f"""
                SELECT tour_name AS item_name, price AS unit_price, agency_id,
                       status, available_slots
                FROM tours
                WHERE id = %s
                {"FOR UPDATE" if for_update else ""}
                """,
                (item_id,),
            )
        else:
            cursor.execute(
                f"""
                SELECT visa_name AS item_name, processing_fee AS unit_price,
                       agency_id, country, status,
                       NULL::INTEGER AS available_slots
                FROM visa_applications
                WHERE id = %s
                {"FOR UPDATE" if for_update else ""}
                """,
                (item_id,),
            )
        item = cursor.fetchone()
        if item is None:
            raise ItemNotFoundError(
                f"{booking_type.value} item {item_id} was not found"
            )
        return item

    @staticmethod
    def _validate_items(cursor, items):
        validated = {}
        for cart_item in items:
            booking_type = BookingType(cart_item["booking_type"])
            item_id = cart_item["item_id"]
            item = CartRepository._get_item(
                cursor, booking_type, item_id, for_update=True
            )
            if str(item["status"]).upper() != "AVAILABLE":
                raise CartItemUnavailableError(
                    f"{booking_type.value} item {item_id} is not available"
                )
            if item["unit_price"] != cart_item["unit_price"]:
                raise CartPriceChangedError(
                    f"Price for {booking_type.value} item {item_id} changed; "
                    "update the cart and try again"
                )
            if (
                booking_type == BookingType.TOUR
                and item["available_slots"] < cart_item["quantity"]
            ):
                raise CartItemUnavailableError(
                    f"Not enough available slots for tour {item_id}"
                )
            validated[(booking_type, item_id)] = item
        return validated

    @staticmethod
    def _cart_for_traveler(cursor, traveler_id: int):
        cursor.execute(
            """
            SELECT
                id, traveler_id, status, total_order_summary,
                created_at, updated_at
            FROM carts
            WHERE traveler_id = %s AND status = %s
            """,
            (traveler_id, CartStatus.ACTIVE.value),
        )
        cart = cursor.fetchone()
        if cart is None:
            return None
        cursor.execute(
            """
            SELECT
                id, cart_id, booking_type, item_id, item_name, quantity,
                unit_price, total_amount, created_at, updated_at
            FROM cart_items
            WHERE cart_id = %s
            ORDER BY created_at, id
            """,
            (cart["id"],),
        )
        return {**dict(cart), "items": [dict(item) for item in cursor.fetchall()]}

    async def get_active_cart(self, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            return self._cart_for_traveler(cursor, traveler_id)
        finally:
            self._close(connection, cursor)

    async def add_item(self, payload, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            item = self._get_item(cursor, payload.booking_type, payload.item_id)
            if str(item["status"]).upper() != "AVAILABLE":
                raise CartItemUnavailableError(
                    f"{payload.booking_type.value} item "
                    f"{payload.item_id} is not available"
                )
            if (
                payload.booking_type == BookingType.TOUR
                and item["available_slots"] < payload.quantity
            ):
                raise CartItemUnavailableError(
                    f"Not enough available slots for tour {payload.item_id}"
                )
            cursor.execute(
                """
                INSERT INTO carts (traveler_id)
                VALUES (%s)
                ON CONFLICT (traveler_id) WHERE status = 'active'
                DO UPDATE SET updated_at = CURRENT_TIMESTAMP
                RETURNING id
                """,
                (traveler_id,),
            )
            cart_id = cursor.fetchone()["id"]
            cursor.execute(
                """
                INSERT INTO cart_items (
                    cart_id, booking_type, item_id, item_name, quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cart_id, booking_type, item_id)
                DO UPDATE SET
                    quantity = cart_items.quantity + EXCLUDED.quantity,
                    item_name = EXCLUDED.item_name,
                    unit_price = EXCLUDED.unit_price,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    cart_id,
                    payload.booking_type.value,
                    payload.item_id,
                    item["item_name"],
                    payload.quantity,
                    item["unit_price"],
                ),
            )
            cart = self._cart_for_traveler(cursor, traveler_id)
            connection.commit()
            return cart
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)

    async def update_item(self, item_id: int, traveler_id: int, quantity: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT ci.cart_id, c.status
                FROM cart_items ci
                JOIN carts c ON c.id = ci.cart_id
                WHERE ci.id = %s AND c.traveler_id = %s
                FOR UPDATE OF ci, c
                """,
                (item_id, traveler_id),
            )
            current = cursor.fetchone()
            if current is None:
                raise CartItemNotFoundError("Cart item not found")
            if current["status"] != CartStatus.ACTIVE.value:
                raise CartNotEditableError("Only active cart items can be changed")

            if quantity == 0:
                cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
                cursor.execute(
                    """
                    DELETE FROM carts
                    WHERE id = %s
                      AND NOT EXISTS (
                          SELECT 1 FROM cart_items WHERE cart_id = %s
                      )
                    """,
                    (current["cart_id"], current["cart_id"]),
                )
            else:
                cursor.execute(
                    """
                    UPDATE cart_items
                    SET quantity = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (quantity, item_id),
                )

            cart = self._cart_for_traveler(cursor, traveler_id)
            connection.commit()
            return cart
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)

    async def delete_item(self, item_id: int, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT ci.cart_id, c.status
                FROM cart_items ci
                JOIN carts c ON c.id = ci.cart_id
                WHERE ci.id = %s AND c.traveler_id = %s
                FOR UPDATE OF ci, c
                """,
                (item_id, traveler_id),
            )
            current = cursor.fetchone()
            if current is None:
                raise CartItemNotFoundError("Cart item not found")
            if current["status"] != CartStatus.ACTIVE.value:
                raise CartNotEditableError("Only active cart items can be removed")

            cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
            cursor.execute(
                """
                DELETE FROM carts
                WHERE id = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM cart_items WHERE cart_id = %s
                  )
                """,
                (current["cart_id"], current["cart_id"]),
            )
            cart = self._cart_for_traveler(cursor, traveler_id)
            connection.commit()
            return cart
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)

    @staticmethod
    def finalize_paid_cart_in_transaction(
        cursor,
        cart_id: int,
        traveler_id: int | None = None,
        expected_amount=None,
    ):
        if traveler_id is None:
            cursor.execute(
                """
                SELECT id, traveler_id, status
                FROM carts
                WHERE id = %s
                FOR UPDATE
                """,
                (cart_id,),
            )
        else:
            cursor.execute(
                """
                SELECT id, traveler_id, status
                FROM carts
                WHERE id = %s AND traveler_id = %s
                FOR UPDATE
                """,
                (cart_id, traveler_id),
            )
        cart = cursor.fetchone()
        if cart is None:
            raise CartNotFoundError("Cart not found")

        if cart["status"] == CartStatus.CHECKED_OUT.value:
            cursor.execute(
                """
                SELECT
                    id, traveler_id, cart_id, booking_reference,
                    total_amount, currency, status, created_at, updated_at
                FROM bookings
                WHERE cart_id = %s
                ORDER BY id
                """,
                (cart_id,),
            )
            return cursor.fetchall()

        if cart["status"] not in (
            CartStatus.ACTIVE.value,
            CartStatus.PENDING_PAYMENT.value,
        ):
            raise CartNotEditableError("Only payable carts can be finalized")

        cursor.execute(
            """
            SELECT
                id, booking_type, item_id, item_name, quantity,
                unit_price, total_amount
            FROM cart_items
            WHERE cart_id = %s
            ORDER BY booking_type, item_id
            FOR UPDATE
            """,
            (cart_id,),
        )
        items = cursor.fetchall()
        if not items:
            raise CartNotEditableError("Cannot finalize an empty cart")
        cart_amount = sum((item["total_amount"] for item in items), 0)
        if expected_amount is not None and cart_amount != expected_amount:
            raise CartPriceChangedError(
                "The cart total no longer matches the payment amount"
            )
        current_items = CartRepository._validate_items(cursor, items)

        created_bookings = []
        for cart_item in items:
            booking_type = BookingType(cart_item["booking_type"])
            item = current_items[(booking_type, cart_item["item_id"])]
            if booking_type == BookingType.TOUR:
                cursor.execute(
                    """
                    UPDATE tours
                    SET available_slots = available_slots - %s,
                        status = CASE
                            WHEN available_slots - %s = 0 THEN 'UNAVAILABLE'
                            ELSE status
                        END,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                      AND UPPER(status) = 'AVAILABLE'
                      AND available_slots >= %s
                    """,
                    (
                        cart_item["quantity"],
                        cart_item["quantity"],
                        cart_item["item_id"],
                        cart_item["quantity"],
                    ),
                )
                if cursor.rowcount != 1:
                    raise CartItemUnavailableError(
                        f"Not enough available slots for tour {cart_item['item_id']}"
                    )

            cursor.execute(
                """
                INSERT INTO bookings (
                    traveler_id, cart_id, booking_reference,
                    total_amount, status
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING
                    id, traveler_id, cart_id, booking_reference,
                    total_amount, currency, status, created_at, updated_at
                """,
                (
                    cart["traveler_id"],
                    cart_id,
                    f"B{uuid4().hex.upper()}",
                    cart_item["total_amount"],
                    BookingStatus.BOOKED.value,
                ),
            )
            booking = cursor.fetchone()

            if booking_type == BookingType.TOUR:
                cursor.execute(
                    """
                    INSERT INTO tour_bookings (
                        booking_id, tour_id, agency_id, tour_name,
                        quantity, unit_price
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        booking["id"],
                        cart_item["item_id"],
                        item["agency_id"],
                        item["item_name"],
                        cart_item["quantity"],
                        cart_item["unit_price"],
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO visa_bookings (
                        booking_id, visa_id, agency_id, visa_name,
                        country, quantity, processing_fee
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        booking["id"],
                        cart_item["item_id"],
                        item["agency_id"],
                        item["item_name"],
                        item["country"],
                        cart_item["quantity"],
                        cart_item["unit_price"],
                    ),
                )
            created_bookings.append(booking)

        cursor.execute(
            """
            UPDATE carts
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (CartStatus.CHECKED_OUT.value, cart_id),
        )
        return created_bookings

    async def finalize_paid_cart(self, cart_id: int):
        """Finalize booking records after payment is manually marked paid."""
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            bookings = self.finalize_paid_cart_in_transaction(cursor, cart_id)
            connection.commit()
            return bookings
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)
