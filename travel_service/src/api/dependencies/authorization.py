from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from services.authentication import verify_access_token


security = HTTPBearer()


async def get_current_agency(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = verify_access_token(token)

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if payload.get("role") != "agency":
        raise HTTPException(
            status_code=403,
            detail="Invalid account type"
        )

    agency_id = payload.get("sub")

    if not agency_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return int(agency_id)
