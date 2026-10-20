from fastapi import HTTPException
from schemas.get_tour_query_request import GetQueryRequest
from services.exception.exceptions import ( 
    TourNotFoundError)
from repository import tour_repository
from schemas.dtos.get_tour_query_response import GetQueryResponse
from models.enums.tour_status import TourStatus


async def get_all_tours(params: GetQueryRequest):
    tours = tour_repository.get_tours(params)

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

    