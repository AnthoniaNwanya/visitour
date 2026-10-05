from fastapi import HTTPException
from schemas.get_query_request import GetQueryRequest
from services.exceptions import ( 
    AgencyNotFoundError)
from repository import agency_repository
from schemas.dtos.get_query_response import GetQueryResponse


async def get_all_agencies(params: GetQueryRequest):
    agencies = agency_repository.get_all_agencies(params)

    if not agencies:
        raise AgencyNotFoundError("Agency with specified parameter not found")
    
    return [
        GetQueryResponse(
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
        status=agency["status"],
        cac_number=agency["cac_number"],
        created_at=agency["created_at"],
        updated_at= agency["updated_at"]
        )
        for agency in agencies
    ]