import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    database=os.getenv("DATABASE_NAME"),
)

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# SQLAlchemy session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# Existing psycopg2 connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        connect_timeout=5,
        options="-c lock_timeout=5000 -c statement_timeout=15000",
    )


def read_from_db(query, params=None):
    conn = get_db_connection()

    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    except Exception as e:
        print(f"Error reading from the database: {e}")
        return None

    finally:
        conn.close()


def write_to_db(query, params=None):
    conn = get_db_connection()

    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error writing to the database: {e}")
        return False

    finally:
        conn.close()


# SQLAlchemy database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
