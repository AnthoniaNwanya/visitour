from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from services.authentications.authentication import verify_access_token


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
            detail="You are not authorized to access this resource."
        )

    agency_id = payload.get("sub")

    try: 
        agency_id = int(agency_id) 
        if agency_id <= 0: 
            raise ValueError 
    except (TypeError, ValueError): 
        raise HTTPException( status_code=401, detail="Invalid token" ) 
    
    return agency_id



async def get_current_user(
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

    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id or role not in {"agency", "traveler"}:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "id": user_id,
        "role": role
    }