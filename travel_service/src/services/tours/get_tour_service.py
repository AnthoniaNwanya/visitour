from fastapi import HTTPException
from schemas.get_query_request import GetQueryRequest
from services.exceptions import ( 
    TourNotFoundError)
from repository import travel_repository
from schemas.dtos.get_query_response import GetQueryResponse


async def get_all_tours(params: GetQueryRequest):
    tours = travel_repository.get_tours(params)

    if not tours:
        raise TourNotFoundError("Tour with specified parameter not found")
    
    return [
        GetQueryResponse(
            id=tour["id"],
            agency_id=tour["agency_id"],
            title=tour["title"],
            description=tour["description"],
            start_date=tour["start_date"],
            end_date=tour["end_date"],
            country=tour["country"],
            price=tour["price"],
            available_slots=tour["available_slots"],
            status=tour["status"],
            created_at=tour["created_at"],
            updated_at= tour["updated_at"]
        )
        for tour in tours
    ]