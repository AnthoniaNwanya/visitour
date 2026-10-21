from fastapi import HTTPException
from schemas.get_tour_query_request import GetQueryRequest
from services.exception.exceptions import ( 
    TourNotFoundError)
from repository import tour_repository
from schemas.dtos.get_tour_query_response import GetQueryResponse
from models.enums.tour_status import TourStatus


async def get_other_agency_tours(params: GetQueryRequest,
    current_agency_id: int):
    tours = tour_repository.get_tours_for_agency_browsing(params, current_agency_id=current_agency_id)

    if not tours:
        raise TourNotFoundError("No tours found with specified parameter")
    
    return [
        GetQueryResponse(
            id=tour["id"],
            agency_id=tour["agency_id"],
            tour_name=tour["tour_name"],
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

async def get_available_tours(params):
    tours = tour_repository.get_tours(
        params,
        status=TourStatus.AVAILABLE
    )
    if not tours:
        raise TourNotFoundError("Tour with specified parameter not found")
    
    return [
        GetQueryResponse(
            id=tour["id"],
            agency_id=tour["agency_id"],
            tour_name=tour["tour_name"],
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


async def get_agency_tours(params, agency_id):
    tours = tour_repository.get_tours(
        params,
        agency_id=agency_id
    )
    if not tours:
        raise TourNotFoundError("Tour with specified parameter not found")

    return [
        GetQueryResponse(
            id=tour["id"],
            agency_id=tour["agency_id"],
            tour_name=tour["tour_name"],
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

    