import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
    )


def read_from_db(query, params=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        connection.close()


def write_to_db(query, params=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
