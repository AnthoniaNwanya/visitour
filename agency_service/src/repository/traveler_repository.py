from psycopg2.extras import DictCursor

from connection import get_db_connection


def get_traveler_id(traveler_id: int):
    connection = get_db_connection()

    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    date_of_birth,
                    address,
                    city,
                    country,
                    nationality,
                    profilepicture,
                    status,
                    created_at,
                    updated_at
                FROM travelers
                WHERE id = %s
                  AND status != %s
                """,
                (traveler_id, "DELETED"),
            )
            return cursor.fetchone()
    finally:
        connection.close()
