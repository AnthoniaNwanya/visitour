from psycopg2.extras import DictCursor

from repository.database.connection import get_db_connection


class BookingRepository:
    async def get_all(self, traveler_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT
                    id, traveler_id, cart_id, booking_reference,
                    total_amount, currency, status, created_at, updated_at
                FROM bookings
                WHERE traveler_id = %s
                ORDER BY created_at DESC
                """,
                (traveler_id,),
            )
            return cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

    async def get_agency_tour_bookings(self, agency_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT
                    tb.id,
                    tb.booking_id,
                    tb.tour_id,
                    tb.tour_name,
                    b.booking_reference,
                    b.traveler_id,
                    tr.first_name AS traveler_first_name,
                    tr.last_name AS traveler_last_name,
                    tr.email AS traveler_email,
                    tb.quantity,
                    tb.unit_price,
                    tb.total_amount,
                    tb.status,
                    tb.created_at,
                    tb.updated_at
                FROM tour_bookings tb
                JOIN bookings b ON b.id = tb.booking_id
                JOIN travelers tr ON tr.id = b.traveler_id
                WHERE tb.agency_id = %s
                ORDER BY tb.created_at DESC, tb.id DESC
                """,
                (agency_id,),
            )
            return cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

    async def get_agency_visa_bookings(self, agency_id: int):
        connection = get_db_connection()
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(
                """
                SELECT
                    vb.id,
                    vb.booking_id,
                    vb.visa_id,
                    vb.visa_name,
                    vb.country,
                    b.booking_reference,
                    b.traveler_id,
                    tr.first_name AS traveler_first_name,
                    tr.last_name AS traveler_last_name,
                    tr.email AS traveler_email,
                    vb.quantity,
                    vb.processing_fee,
                    vb.total_amount,
                    vb.status,
                    vb.created_at,
                    vb.updated_at
                FROM visa_bookings vb
                JOIN bookings b ON b.id = vb.booking_id
                JOIN travelers tr ON tr.id = b.traveler_id
                WHERE vb.agency_id = %s
                ORDER BY vb.created_at DESC, vb.id DESC
                """,
                (agency_id,),
            )
            return cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()
