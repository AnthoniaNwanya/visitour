from fastapi import HTTPException
from api.dependencies.authorization import get_current_agency
from schemas.update_agency_request import UpdateAgencyRequest
from services.exceptions import ( 
    AgencyNotFoundError, 
    AgencyAlreadyExistsError,
    ValueRequiredError,
    VerifyMismatchError)
from repository import agency_repository
from schemas.dtos.update_agency_response import UpdateAgencyResponse
from argon2 import PasswordHasher

async def update_agency(request: UpdateAgencyRequest, agency_id: int):
# authorize agency by logging in before this request

    existing_id = agency_repository.get_agency_id(agency_id)
    if not existing_id:
        raise AgencyNotFoundError("Agency not found")

    if request.agency_name:
        existing_name = agency_repository.get_agency_name(request.agency_name)

        if existing_name and existing_name["id"] != agency_id:
            raise AgencyAlreadyExistsError("An agency with this name already exists")
    
    if request.password and not request.confirm_password:
        raise ValueRequiredError("Confirm Password is required")

    if request.confirm_password and not request.password:
        raise ValueRequiredError("Password is required")

    if request.password != request.confirm_password:
        raise VerifyMismatchError("Password and Confirm Password do not match")
    
    password_hash = None

    if request.password:
        password_hasher = PasswordHasher()
        password_hash = password_hasher.hash(request.password)

    agency = agency_repository.update_agency(
        agency_id, 
        request,
        password_hash
    )

    return UpdateAgencyResponse(
        id=agency["id"],
        agency_name=agency["agency_name"],
        description=agency["description"],
        first_name=agency["first_name"],
        last_name=agency["last_name"],
        email=agency["email"],
        phone_number=agency["phone_number"],
        address=agency["address"],
        country=agency["country"],
        city=agency["city"],
        cac_number=agency["cac_number"],
        status=agency["status"],
        updated_at=agency["updated_at"]
    )