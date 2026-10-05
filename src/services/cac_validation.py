import os
import re

import httpx
from fastapi import HTTPException

from schemas.validate_cac_request import ValidateCACRequest
from services.verify_agency import approve_agency, reject_agency
from repository import agency_repository
from services.exceptions import AgencyAlreadyExistsError, AgencyNotFoundError


KORAPAY_CAC_URL = (
    "https://api.korapay.com/merchant/api/v1/identities/ng/cac"
)

KORAPAY_SECRET_KEY = os.getenv("KORAPAY_SECRET_KEY")


def _normalize_cac_id(value: str) -> str:
    """
    Convert RC00000011 -> 00000011
    """

    cleaned = re.sub(r"\D", "", value or "")

    if not cleaned:
        raise HTTPException(
            status_code=400,
            detail="Invalid CAC number"
        )

    return cleaned


async def validate_cac(agency_id: int, request: ValidateCACRequest):
    existing_agent = agency_repository.get_agency_id(agency_id)
    if not existing_agent:
        raise AgencyNotFoundError("Agency not found")
    
    existing_cac = agency_repository.get_cac(request.cac_number)
    if existing_cac and existing_cac["id"] != agency_id:
        raise AgencyAlreadyExistsError(
            "An Agency with this CAC already exists. "      
        )
    
    if not KORAPAY_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="CAC verification is not configured"
        )

    cac_id = _normalize_cac_id(request.cac_number)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                KORAPAY_CAC_URL,
                headers={
                    "Authorization": (
                        f"Bearer {KORAPAY_SECRET_KEY}"
                    ),
                    "Content-Type": "application/json"
                },
                json={
                    "id": cac_id,
                    "registration_type": "RC",
                    "verification_consent": True
                }
            )

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "CAC verification service is unreachable. "
                "Please try again later."
            )
        ) from exc

    if response.status_code in {404, 422}:
        return await reject_agency(agency_id, request.cac_number)

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="CAC verification failed. Please try again later."
        )

    body = response.json()

    if not body.get("status"):
        return await reject_agency(agency_id, request.cac_number)

    data = body.get("data")

    if not data:
        raise HTTPException(
            status_code=502,
            detail="CAC verification returned an unexpected response."
        )

    company_status = (
        data.get("company_status") or ""
    ).upper()

    if company_status != "ACTIVE":
        return await reject_agency(
        agency_id,
        request.cac_number
    )

    return await approve_agency(
        agency_id,
        request.cac_number
    )