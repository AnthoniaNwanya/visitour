from fastapi import HTTPException, Depends
from schemas.update_tour_request import UpdateTourRequest
from services.exceptions import ( 
    TourNotFoundError, 
    TourAlreadyExistsError)
from repository import travel_repository
from schemas.dtos.update_tour_response import UpdateTourResponse
from api.dependencies.authorization import get_current_agency


async def update_tour(request: UpdateTourRequest, tour_id: int, agency_id: int = Depends(get_current_agency)):
    existing_id = travel_repository.get_tour_id(tour_id)
    if not existing_id:
        raise TourNotFoundError("Tour not found")

    existing_title = travel_repository.get_tour_by_title(
        request.title,
        agency_id
    )

    if existing_title and existing_title["id"] != tour_id:
        raise TourAlreadyExistsError(
            "You already have a tour with this name."
        )

    tour = travel_repository.update_tour(
        request,
        tour_id
    )

    return UpdateTourResponse(
        id=tour["id"],
        agency_id=tour["agency_id"],
        title=tour["title"],
        description=tour["description"],
        country=tour["country"],
        start_date=tour["start_date"],
        end_date=tour["end_date"],
        price=tour["price"],
        available_slots=tour["available_slots"],
        status=tour["status"],
        updated_at=tour["updated_at"]
    )