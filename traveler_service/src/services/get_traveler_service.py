from fastapi import HTTPException
from schemas.get_traveler_query_request import GetTravelerQueryRequest
from services.exception.exceptions import ( 
    TravelerNotFoundError,
    ForbiddenError)
from repository import traveler_repository
from schemas.dtos.get_traveler_query_response import GetTravelerQueryResponse

async def get_travelers(params: GetTravelerQueryRequest):
    travelers = traveler_repository.get_all_travelers(params)
    if not travelers:
        raise TravelerNotFoundError("Traveler not found")
    
    return [
        GetTravelerQueryResponse(
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
        created_at=traveler["created_at"],
        updated_at= traveler["updated_at"]
        )
        for traveler in travelers
    ]

async def get_traveler_for_traveler(current_traveler_id):
    traveler = traveler_repository.get_traveler_id(current_traveler_id)
    if not traveler:
        raise ForbiddenError("Traveler not found")
    
    return GetTravelerQueryResponse(
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
        created_at=traveler["created_at"],
        updated_at= traveler["updated_at"]
        )

async def get_traveler_for_agency(traveler_id: int):
    traveler = traveler_repository.get_traveler_id(traveler_id)

    if not traveler:
        raise ForbiddenError("Traveler not found")
    
    return GetTravelerQueryResponse(
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
        created_at=traveler["created_at"],
        updated_at= traveler["updated_at"]
    )