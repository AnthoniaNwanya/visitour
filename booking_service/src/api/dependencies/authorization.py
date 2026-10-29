from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from services.authentications.authentication import verify_access_token


security = HTTPBearer()


async def get_current_traveler(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    try:
        payload = verify_access_token(credentials.credentials)
    except JWTError as exc:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token"
        ) from exc

    if payload.get("role") != "traveler":
        raise HTTPException(
            status_code=403,
            detail="Only travelers can access this resource",
        )

    try:
        traveler_id = int(payload.get("sub"))
        if traveler_id <= 0:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    return traveler_id


async def get_current_agency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    try:
        payload = verify_access_token(credentials.credentials)
    except JWTError as exc:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token"
        ) from exc

    if payload.get("role") != "agency":
        raise HTTPException(
            status_code=403,
            detail="Only agencies can access this resource",
        )

    try:
        agency_id = int(payload.get("sub"))
        if agency_id <= 0:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    return agency_id
