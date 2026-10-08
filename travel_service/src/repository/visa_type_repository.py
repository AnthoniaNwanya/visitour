from repository.database.connection import get_db_connection
from psycopg2.extras import DictCursor


def get_all():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    cursor.execute("""
        SELECT
            id,
            name,
            description,
            created_at,
            updated_at
        FROM visa_types
        ORDER BY name
    """)

    visa_types = cursor.fetchall()

    cursor.close()
    connection.close()

    return visa_types


def get_by_id(visa_type_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    cursor.execute("""
        SELECT
            id,
            name,
            description,
            created_at,
            updated_at
        FROM visa_types
        WHERE id = %s
    """, (visa_type_id,))

    visa_type = cursor.fetchone()

    cursor.close()
    connection.close()

    return visa_type