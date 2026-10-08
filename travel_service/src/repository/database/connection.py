import os 

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def read_from_db(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error reading from the database: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def write_to_db(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error writing to the database: {e}")
        return False
    finally:
        cursor.close()
        conn.close()