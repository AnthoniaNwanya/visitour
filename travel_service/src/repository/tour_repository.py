from repository.database.connection import get_db_connection
from models.enums.tour_status import TourStatus
from psycopg2.extras import DictCursor
from datetime import timedelta

def create(request, agency_id: int, status: TourStatus,):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        INSERT INTO tours (
            agency_id,
            title,
            description,
            country,
            start_date,
            end_date,
            price,
            available_slots,
            status
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        RETURNING
            id,
            agency_id,
            title,
            description,
            country,
            start_date,
            end_date,
            price,
            available_slots,
            status,
            created_at
    """
    cursor.execute(
        query,
        (
            agency_id,
            request.title,
            request.description,
            request.country,
            request.start_date,
            request.end_date,
            request.price,
            request.available_slots,
            status.value
        )
    )
    tour = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return tour

def get_tours(params):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_id,
            title,
            description,
            start_date,
            end_date,
            country,
            price,
            available_slots,                                                                        
            status,
            created_at,
            updated_at
        FROM tours
        WHERE 1 = 1
        
    """
    values = []

    if params.id is not None:
        query += " AND id = %s"
        values.append(params.id)

    if params.title:
        query += " AND %s = ANY(title) "
        values.append(params.title)

    if params.country:
        query += " AND %s = ANY(country)"
        values.append(params.country)

    if params.start_date:
        query += " AND start_date = %s"
        values.append(params.start_date)

    if params.end_date:
        query += " AND end_date = %s"
        values.append(params.end_date)

    if params.available_slots is not None:
        query += " AND available_slots = %s"
        values.append(params.available_slots)

    if params.status:
        query += " AND status = %s"
        values.append(params.status)

    if params.min_price is not None:
        query += " AND price >= %s"
        values.append(params.min_price)

    if params.max_price is not None:
        query += " AND price <= %s"
        values.append(params.max_price)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)

    tours = cursor.fetchall()

    cursor.close()
    connection.close()

    return tours

def get_tour_id(tour_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_id,
            title,
            description,
            start_date,
            end_date,
            country,
            price,
            available_slots,                                                                        
            status,
            created_at,
            updated_at
        FROM tours
        WHERE id = %s
    
    """

    cursor.execute(query, (tour_id,))

    tour = cursor.fetchone()

    cursor.close()
    connection.close()

    return tour

def get_tour_by_title(title: str, agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT id, agency_id, title
        FROM tours
        WHERE title = %s
        AND agency_id = %s
    """

    cursor.execute(query, (title, agency_id))

    tour = cursor.fetchone()

    cursor.close()
    connection.close()

    return tour


def update_tour(request, tour_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    data = request.model_dump(exclude_unset=True)

    if not data:
        cursor.execute(
            """
            SELECT
                id,
                agency_id,
                title,
                description,
                country,
                start_date,
                end_date,
                price,
                available_slots,
                status,
                updated_at
            FROM tours
            WHERE id = %s
            """,
            (tour_id,)
        )

        tour = cursor.fetchone()

        cursor.close()
        connection.close()

        return tour

    allowed_fields = {
        "title",
        "description",
        "country",
        "start_date",
        "end_date",
        "price",
        "available_slots",
        "status"
    }

    data = {
        field: value
        for field, value in data.items()
        if field in allowed_fields
    }

    fields = []
    values = []

    for field, value in data.items():
        fields.append(f"{field} = %s")
        values.append(value)

    fields.append("updated_at = CURRENT_TIMESTAMP")

    values.append(tour_id)

    query = f"""
        UPDATE tours
        SET
            {", ".join(fields)}
        WHERE id = %s
        RETURNING
            id,
            agency_id,
            title,
            description,
            country,
            start_date,
            end_date,
            price,
            available_slots,
            status,
            updated_at
    """

    cursor.execute(query, values)

    tour = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return tour

def delete_tour(tour_id: int, agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        DELETE FROM tours
        WHERE 
            id = %s
        AND
            agency_id = %s
        RETURNING
            id,
            agency_id,
            title,
            description,
            country,
            start_date,
            end_date,
            price,
            available_slots,
            status,
            updated_at
    """

    cursor.execute(
        query,
        (
            tour_id,
            agency_id,
        )
    )

    tour = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return tour

