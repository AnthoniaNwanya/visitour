from repository.database.connection import get_db_connection
from models.enums.traveler_status import TravelerStatus
from psycopg2.extras import DictCursor
from datetime import timedelta

def create(request, password_hash: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        INSERT INTO travelers (
            first_name,
            last_name,
            email,
            phone_number,
            password_hash,
            date_of_birth,
            address,
            city,
            country,
            nationality
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        RETURNING
            id,
            first_name,
            last_name,
            email,
            phone_number,
            password_hash,
            date_of_birth,
            address,
            city,
            country,
            nationality,
            status,
            created_at
    """
    cursor.execute(
        query,
        (
            request.first_name,
            request.last_name,
            request.email,
            request.phone_number,
            password_hash,
            request.date_of_birth,
            request.address,
            request.city,
            request.country,
            request.nationality
        )
    )
    traveler = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return traveler

def get_all_travelers(params):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
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
            status,
            created_at,
            updated_at
        FROM travelers
        WHERE status != %s 
        
    """
    values = [TravelerStatus.DELETED.value]
    if params.id is not None:
        query += " AND id = %s"
        values.append(params.id)

    if params.first_name:
        query += " AND %s = ANY(first_name)"
        values.append(params.first_name)

    if params.last_name:
        query += " AND %s = ANY(last_name)"
        values.append(params.last_name)

    if params.city:
        query += " AND %s = ANY(city)"
        values.append(params.city)

    if params.country:
        query += " AND country = %s"
        values.append(params.country)

    if params.nationality:
        query += " AND nationality = %s"
        values.append(params.nationality)

    if params.status:
        query += " AND status = %s"
        values.append(params.status)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)

    travelers = cursor.fetchall()

    cursor.close()
    connection.close()

    return travelers

def get_traveler_id(traveler_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
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
            status,
            created_at,
            updated_at
        FROM travelers
        WHERE id = %s
        AND
        status != %s 
    """

    cursor.execute(query, (traveler_id, TravelerStatus.DELETED.value,))

    agency = cursor.fetchone()

    cursor.close()
    connection.close()

    return agency

def get_traveler_by_email(email):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        SELECT * 
        FROM travelers 
        WHERE email = %s
        AND status != %s
       
    """
    cursor.execute(query, (email, TravelerStatus.DELETED.value))

    traveler = cursor.fetchone()

    cursor.close()
    connection.close()

    return traveler

def update_traveler(request, current_traveler_id: int, password_hash=None):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    data = request.model_dump(exclude_unset=True)

    data.pop("confirm_password", None)

    if password_hash:
        data["password_hash"] = password_hash

    if not data:
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
                status,
                created_at,
                updated_at
            FROM travelers
            WHERE id = %s
            """,
            (current_traveler_id,)
        )

        traveler = cursor.fetchone()

        cursor.close()
        connection.close()

        return traveler

    allowed_fields = {
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "password_hash",
        "date_of_birth",
        "address",
        "city",
        "country",
        "nationality",
        "status",
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

    values.append(current_traveler_id)

    query = f"""
        UPDATE travelers
        SET
            {", ".join(fields)}
        WHERE id = %s
        RETURNING
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
            status,
            updated_at
    """

    cursor.execute(query, values)

    traveler = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return traveler

def delete_traveler(current_traveler_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        DELETE FROM travelers
        WHERE 
            id = %s
        RETURNING
            id,
            first_name,
            last_name,
            email,
            phone_number,
            password_hash,
            date_of_birth,
            address,
            city,
            country,
            nationality,
            status,
            created_at,
            updated_at
    """

    cursor.execute(
        query,
        (
            current_traveler_id,
        )
    )

    traveler = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return traveler

