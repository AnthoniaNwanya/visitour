from fastapi import HTTPException
from schemas.update_traveler_request import UpdateTravelerRequest
from services.exception.exceptions import ( 
    TravelerNotFoundError, 
    ValueRequiredError,
    VerifyMismatchError,
    TravelerAlreadyExistsError)
from repository import traveler_repository
from schemas.dtos.update_traveler_response import UpdateTravelerResponse
from argon2 import PasswordHasher

async def update_traveler(request: UpdateTravelerRequest, current_traveler_id: int):
    existing_id = traveler_repository.get_traveler_id(current_traveler_id)
    if not existing_id:
        raise TravelerNotFoundError("Traveler not found")

    existing_email = traveler_repository.get_traveler_by_email(request.email)
    if existing_email:
        raise TravelerAlreadyExistsError("Traveler with this email already exists")
    
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

    traveler = traveler_repository.update_traveler(
        request,
        current_traveler_id, 
        password_hash
    )

    return UpdateTravelerResponse(
        id=traveler["id"],
        first_name=traveler["first_name"],
        last_name=traveler["last_name"],
        email=traveler["email"],
        phone_number=traveler["phone_number"],
        date_of_birth=traveler["date_of_birth"],
        address=traveler["address"],
        city=traveler["city"],
        country=traveler["country"],
        nationality=traveler["nationality"],
        status=traveler["status"],
        updated_at=traveler["updated_at"]
    )