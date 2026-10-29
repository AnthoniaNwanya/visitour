import os
from pathlib import Path

from dotenv import load_dotenv
from jose import jwt


BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"


def verify_access_token(token: str):
    if not AUTH_SECRET_KEY:
        raise RuntimeError("AUTH_SECRET_KEY is not configured")
    return jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
