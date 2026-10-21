from repository.database.connection import get_db_connection
from models.enums.visa_status import VisaStatus
from psycopg2.extras import DictCursor
from datetime import timedelta

def create(request, agency_id: int, status: VisaStatus,):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        INSERT INTO visa_applications (
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status
        
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        RETURNING
            id,
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status,
            created_at
    """
    cursor.execute(
        query,
        (
            agency_id,
            request.visa_name,
            request.country,
            request.visa_type_id,
            request.processing_time_value,
            request.processing_time_unit,
            request.processing_fee,
            status.value
        )
    )
    visa_application = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return visa_application

def get_visas(params, agency_id=None, status=None):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status,
            created_at,
            updated_at
        FROM visa_applications
        WHERE 1 = 1
        
    """
    values = []

    if agency_id is not None:
        query += " AND agency_id = %s"
        values.append(agency_id)

    if status is not None:
        query += " AND status = %s"
        values.append(status)

    if params.id is not None:
        query += " AND id = %s"
        values.append(params.id)

    if params.visa_name:
        query += " AND %s = ANY(visa_name) "
        values.append(params.visa_name)

    if params.country:
        query += " AND %s = ANY(country)"
        values.append(params.country)

    if params.visa_type_id is not None:
        query += " AND visa_type_id = %s"
        values.append(params.visa_type_id)

    if params.status:
        query += " AND status = %s"
        values.append(params.status)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)

    visa_applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return visa_applications

def get_visas_for_agency_browsing(
    params,
    current_agency_id: int
):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status,
            created_at,
            updated_at
        FROM visa_applications
        WHERE (
            agency_id = %s
            OR status = %s
        )
    """

    values = [
        current_agency_id,
        VisaStatus.AVAILABLE.value
    ]

    if params.id is not None:
        query += " AND id = %s"
        values.append(params.id)

    if params.visa_name:
        query += " AND %s = ANY(visa_name) "
        values.append(params.visa_name)

    if params.country:
        query += " AND %s = ANY(country)"
        values.append(params.country)

    if params.visa_type_id is not None:
        query += " AND visa_type_id = %s"
        values.append(params.visa_type_id)

    if params.status:
        status = (
            params.status.value
            if hasattr(params.status, "value")
            else params.status
        )
        query += " AND status = %s"
        values.append(status)

    query += " ORDER BY created_at DESC"

    try:
        cursor.execute(query, tuple(values))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_visa_id(visa_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status,
            created_at,
            updated_at
        FROM visa_applications
        WHERE id = %s
    
    """

    cursor.execute(query, (visa_id,))

    visa_application = cursor.fetchone()

    cursor.close()
    connection.close()

    return visa_application

def get_visa_by_name(visa_name: str, agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT id, agency_id, visa_name
        FROM visa_applications
        WHERE visa_name = %s
        AND agency_id = %s
    """

    cursor.execute(query, (visa_name, agency_id))

    visa_application = cursor.fetchone()

    cursor.close()
    connection.close()

    return visa_application



def update_visa(request, visa_id: int, agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    try:
        data = request.model_dump(exclude_unset=True)

        allowed_fields = {
            "visa_name",
            "country",
            "visa_type_id",
            "processing_time_value",
            "processing_time_unit",
            "processing_fee",
            "status"
        }

        data = {
            field: value
            for field, value in data.items()
            if field in allowed_fields
        }

        # If no fields were provided, return the visa only
        # if it belongs to the authenticated agency.
        if not data:
            cursor.execute(
                """
                SELECT
                    id,
                    agency_id,
                    visa_name,
                    country,
                    visa_type_id,
                    processing_time_value,
                    processing_time_unit,
                    processing_fee,
                    status,
                    updated_at
                FROM visa_applications
                WHERE id = %s
                  AND agency_id = %s
                """,
                (visa_id, agency_id)
            )

            return cursor.fetchone()

        fields = []
        values = []

        for field, value in data.items():
            fields.append(f"{field} = %s")

            # Convert enum values if the status is an Enum.
            if hasattr(value, "value"):
                value = value.value

            values.append(value)

        fields.append("updated_at = CURRENT_TIMESTAMP")

        # Both conditions are required.
        values.extend([visa_id, agency_id])

        query = f"""
            UPDATE visa_applications
            SET {", ".join(fields)}
            WHERE id = %s
              AND agency_id = %s
            RETURNING
                id,
                agency_id,
                visa_name,
                country,
                visa_type_id,
                processing_time_value,
                processing_time_unit,
                processing_fee,
                status,
                updated_at
        """

        cursor.execute(query, values)
        visa_application = cursor.fetchone()

        if visa_application:
            connection.commit()

        return visa_application

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_visa(visa_id: int, agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        DELETE FROM visa_applications
        WHERE 
            id = %s
        AND
            agency_id = %s
        RETURNING
            id,
            agency_id,
            visa_name,
            country,
            visa_type_id,
            processing_time_value,
            processing_time_unit,
            processing_fee,
            status,
            updated_at
    """

    cursor.execute(
        query,
        (
            visa_id,
            agency_id,
        )
    )

    visa = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return visa

