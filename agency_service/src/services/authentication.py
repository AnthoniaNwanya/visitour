from datetime import datetime, timedelta, timezone
import os
from jose import jwt


AUTH_SECRET_KEY =  os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(agency_id: int, role: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(agency_id),
        "role": "agency",
        "exp": expire
    }

    return jwt.encode(
        payload,
        AUTH_SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(token: str):
    return jwt.decode(
        token,
        AUTH_SECRET_KEY,
        algorithms=[ALGORITHM]
    )