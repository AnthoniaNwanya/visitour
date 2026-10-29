from uuid import uuid4

from psycopg2.extras import DictCursor

from models.enums.cart_status import CartStatus
from models.enums.payment_status import PaymentStatus
from repository.cart_repository import CartRepository
from repository.database.connection import get_db_connection
from services.exception.exceptions import (
    CartNotEditableError,
    CartNotFoundError,
    CartPriceChangedError,
    PaymentNotEditableError,
    PaymentNotFoundError,
)


class PaymentRepository:
    @staticmethod
    def _close(connection, cursor, rollback=False):
        if rollback:
            connection.rollback()
        if cursor is not None:
            cursor.close()
        connection.close()

    @staticmethod
    def _select_fields():
        return """
            p.id, p.cart_id, p.payment_reference, p.amount, p.currency,
            p.status, p.payment_method, p.created_at, p.updated_at
        """

    async def create(self, cart_id: int, traveler_id: int, payment_method: str):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT id, status
                FROM carts
                WHERE id = %s AND traveler_id = %s
                FOR UPDATE
                """,
                (cart_id, traveler_id),
            )
            cart = cursor.fetchone()
            if cart is None:
                raise CartNotFoundError("Cart not found")

            if cart["status"] == CartStatus.PENDING_PAYMENT.value:
                cursor.execute(
                    f"""
                    SELECT {self._select_fields()}
                    FROM payments p
                    WHERE p.cart_id = %s AND p.status = %s
                    """,
                    (cart_id, PaymentStatus.PENDING.value),
                )
                payment = cursor.fetchone()
                if payment is None:
                    raise CartNotEditableError(
                        "This cart already has a checkout in progress"
                    )
                connection.commit()
                return payment

            if cart["status"] != CartStatus.ACTIVE.value:
                raise CartNotEditableError("Only active carts can be checked out")

            cursor.execute(
                """
                SELECT
                    booking_type, item_id, quantity, unit_price, total_amount
                FROM cart_items
                WHERE cart_id = %s
                ORDER BY booking_type, item_id
                FOR UPDATE
                """,
                (cart_id,),
            )
            items = cursor.fetchall()
            if not items:
                raise CartNotEditableError("Cannot create payment for an empty cart")

            CartRepository._validate_items(cursor, items)
            cursor.execute(
                """
                SELECT COALESCE(SUM(total_amount), 0) AS amount
                FROM cart_items
                WHERE cart_id = %s
                """,
                (cart_id,),
            )
            amount = cursor.fetchone()["amount"]
            cursor.execute(
                """
                INSERT INTO payments (
                    cart_id, payment_reference, amount, currency, status,
                    payment_method
                )
                VALUES (%s, %s, %s, 'NGN', %s, %s)
                RETURNING
                    id, cart_id, payment_reference, amount, currency, status,
                    payment_method, created_at, updated_at
                """,
                (
                    cart_id,
                    f"P{uuid4().hex.upper()}",
                    amount,
                    PaymentStatus.PENDING.value,
                    payment_method,
                ),
            )
            payment = cursor.fetchone()
            cursor.execute(
                """
                UPDATE carts
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (CartStatus.PENDING_PAYMENT.value, cart_id),
            )
            connection.commit()
            return payment
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)

    async def get_all(self, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                f"""
                SELECT {self._select_fields()}
                FROM payments p
                JOIN carts c ON c.id = p.cart_id
                WHERE c.traveler_id = %s
                ORDER BY p.created_at DESC, p.id DESC
                """,
                (traveler_id,),
            )
            return cursor.fetchall()
        finally:
            self._close(connection, cursor)

    async def get_by_id(self, payment_id: int, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                f"""
                SELECT {self._select_fields()}
                FROM payments p
                JOIN carts c ON c.id = p.cart_id
                WHERE p.id = %s AND c.traveler_id = %s
                """,
                (payment_id, traveler_id),
            )
            return cursor.fetchone()
        finally:
            self._close(connection, cursor)

    async def update(
        self,
        payment_id: int,
        traveler_id: int,
        status: str | None,
        payment_method: str | None,
    ):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                f"""
                SELECT {self._select_fields()}, c.status AS cart_status
                FROM payments p
                JOIN carts c ON c.id = p.cart_id
                WHERE p.id = %s AND c.traveler_id = %s
                FOR UPDATE OF p, c
                """,
                (payment_id, traveler_id),
            )
            payment = cursor.fetchone()
            if payment is None:
                raise PaymentNotFoundError("Payment not found")

            if payment["status"] != PaymentStatus.PENDING.value:
                if (
                    status == payment["status"]
                    and (
                        payment_method is None
                        or payment_method == payment["payment_method"]
                    )
                ):
                    connection.commit()
                    return payment
                raise PaymentNotEditableError(
                    "Only pending payments can be changed"
                )

            if status == PaymentStatus.PAID.value:
                CartRepository.finalize_paid_cart_in_transaction(
                    cursor,
                    payment["cart_id"],
                    traveler_id,
                    payment["amount"],
                )
            elif status in (
                PaymentStatus.FAILED.value,
                PaymentStatus.CANCELLED.value,
            ):
                if payment["cart_status"] == CartStatus.PENDING_PAYMENT.value:
                    cursor.execute(
                        """
                        UPDATE carts
                        SET status = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (CartStatus.ACTIVE.value, payment["cart_id"]),
                    )

            cursor.execute(
                """
                UPDATE payments
                SET status = COALESCE(%s, status),
                    payment_method = COALESCE(%s, payment_method),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id, cart_id, payment_reference, amount, currency, status,
                    payment_method, created_at, updated_at
                """,
                (status, payment_method, payment_id),
            )
            updated_payment = cursor.fetchone()
            connection.commit()
            return updated_payment
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)

    async def delete(self, payment_id: int, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT p.status, p.cart_id, c.status AS cart_status
                FROM payments p
                JOIN carts c ON c.id = p.cart_id
                WHERE p.id = %s AND c.traveler_id = %s
                FOR UPDATE OF p, c
                """,
                (payment_id, traveler_id),
            )
            payment = cursor.fetchone()
            if payment is None:
                raise PaymentNotFoundError("Payment not found")
            if payment["status"] == PaymentStatus.PAID.value:
                raise PaymentNotEditableError("Paid payments cannot be deleted")

            cursor.execute("DELETE FROM payments WHERE id = %s", (payment_id,))
            if (
                payment["status"] == PaymentStatus.PENDING.value
                and payment["cart_status"] == CartStatus.PENDING_PAYMENT.value
            ):
                cursor.execute(
                    """
                    UPDATE carts
                    SET status = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (CartStatus.ACTIVE.value, payment["cart_id"]),
                )
            connection.commit()
        except Exception:
            self._close(connection, cursor, rollback=True)
            raise
        finally:
            if not connection.closed:
                self._close(connection, cursor)
