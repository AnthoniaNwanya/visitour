from datetime import datetime, timedelta, timezone
import os
from jose import jwt
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

AUTH_SECRET_KEY =  os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"


def verify_access_token(token: str):
    return jwt.decode(
        token,
        AUTH_SECRET_KEY,
        algorithms=[ALGORITHM]
    )