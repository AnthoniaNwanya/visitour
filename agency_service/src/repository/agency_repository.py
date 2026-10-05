from repository.database.connection import get_db_connection
from models.enums.agency_status import AgencyStatus
from psycopg2.extras import DictCursor
from datetime import timedelta

def create(request, status: AgencyStatus, password_hash: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        INSERT INTO agencies (
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            password_hash
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s,%s, %s, %s, %s, %s
        )
        RETURNING
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            created_at
    """
    cursor.execute(
        query,
        (
            request.agency_name,
            request.description,
            request.first_name,
            request.last_name,
            request.email,
            request.phone_number,
            request.address,
            request.country,
            request.city,
            status.value,
            request.cac_number,
            password_hash
        )
    )
    agency = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return agency

def get_all_agencies(params):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            created_at,
            updated_at
        FROM agencies
        WHERE status != %s 
        
    """
    values = [AgencyStatus.DELETED.value]
    if params.id is not None:
        query += " AND id = %s"
        values.append(params.id)

    if params.agency_name:
        query += " AND agency_name = %s"
        values.append(params.agency_name)

    if params.email:
        query += " AND email = %s"
        values.append(params.email)

    if params.country:
        query += " AND country = %s"
        values.append(params.country)

    if params.city:
        query += " AND city = %s"
        values.append(params.city)

    if params.status:
        query += " AND status = %s"
        values.append(params.status)

    if params.cac_number:
        query += " AND cac_number = %s"
        values.append(params.cac_number)

    if params.start_date:
        query += " AND created_at >= %s"
        values.append(params.start_date)

    if params.end_date:
        query += " AND created_at < %s"
        values.append(params.end_date + timedelta(days=1))

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)

    agencies = cursor.fetchall()

    cursor.close()
    connection.close()

    return agencies

def get_agency_id(agency_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        SELECT
            id,
            agency_name,
            description,
            email,
            phone_number,
            address,
            country,
            city,
            cac_number,
            status,
            created_at
        FROM agencies
        WHERE id = %s
        AND
        status != %s 
    """

    cursor.execute(query, (agency_id, AgencyStatus.DELETED.value,))

    agency = cursor.fetchone()

    cursor.close()
    connection.close()

    return agency

def get_agency_email(email):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)
    query = """
        SELECT * 
        FROM agencies 
        WHERE email = %s
        AND status != %s
    """
    cursor.execute(query, (email, AgencyStatus.DELETED.value,))

    agency = cursor.fetchone()

    cursor.close()
    connection.close()

    return agency

def get_agency_name(agency_name):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)
    
    query = """
        SELECT * 
        FROM agencies 
        WHERE agency_name = %s
        AND status != %s 
    """
    cursor.execute(query, (agency_name, AgencyStatus.DELETED.value,))

    agency = cursor.fetchone()

    cursor.close()
    connection.close()

    return agency

def update_agency(agency_id: int, request, password_hash=None):
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
                agency_name,
                description,
                first_name,
                last_name,
                email,
                phone_number,
                address,
                country,
                city,
                status,
                cac_number,
                updated_at
            FROM agencies
            WHERE id = %s
            """,
            (agency_id,)
        )

        agency = cursor.fetchone()

        cursor.close()
        connection.close()

        return agency

    allowed_fields = {
        "agency_name",
        "description",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "country",
        "city",
        "password_hash",
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

    values.append(agency_id)

    query = f"""
        UPDATE agencies
        SET
            {", ".join(fields)}
        WHERE id = %s
        RETURNING
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            updated_at
    """

    cursor.execute(query, values)

    agency = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return agency

def delete_agency(agency_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        UPDATE agencies
        SET
            status = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE 
            id = %s
        RETURNING
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            updated_at
    """

    cursor.execute(
        query,
        (
            AgencyStatus.DELETED.value,
            agency_id
        )
    )

    agency = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return agency


def accept_cac(agency_id: int, cac_number: str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        UPDATE agencies
        SET
            status = %s,
            cac_number = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE 
            id = %s
        RETURNING
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            created_at
    """

    cursor.execute(
        query,
        (
            AgencyStatus.ACTIVE.value,
            cac_number,
            agency_id
        )
    )

    agency = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return agency

def reject_cac(agency_id: int, cac_number:str):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=DictCursor)

    query = """
        UPDATE agencies
        SET
            status = %s,
            cac_number = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE 
            id = %s
        RETURNING
            id,
            agency_name,
            description,
            first_name,
            last_name,
            email,
            phone_number,
            address,
            country,
            city,
            status,
            cac_number,
            created_at
    """

    cursor.execute(
        query,
        (
            AgencyStatus.REJECTED.value,
            cac_number,
            agency_id
        )
    )

    agency = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return agency

def get_cac(cac_number:str):
    connection = get_db_connection()

    cursor = connection.cursor(cursor_factory=DictCursor)

    cursor.execute("SELECT * FROM agencies WHERE cac_number = %s", (cac_number,))

    agency = cursor.fetchone()

    cursor.close()
    connection.close()

    return agency