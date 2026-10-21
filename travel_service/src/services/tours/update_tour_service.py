from fastapi import HTTPException, Depends
from schemas.update_tour_request import UpdateTourRequest
from services.exception.exceptions import ( 
    TourNotFoundError, 
    TourAlreadyExistsError,
    UnauthorizedError)
from repository import tour_repository
from schemas.dtos.update_tour_response import UpdateTourResponse
from api.dependencies.authorization import get_current_agency


async def update_tour(request: UpdateTourRequest, tour_id: int, agency_id: int):
    existing_tour = tour_repository.get_tour_id(tour_id)
    if not existing_tour:
        raise TourNotFoundError("Tour not found")

    if existing_tour["agency_id"] != agency_id:
        raise UnauthorizedError(
            "You are not authorized to update this tour"
        )

    # Check duplicate titles only when a new title is provided.
    if request.title is not None:
        existing_title = tour_repository.get_tour_by_title(
            request.title,
            agency_id
        )

        if existing_title and existing_title["id"] != tour_id:
            raise TourAlreadyExistsError(
                "You already have a tour with this title."
            )

    tour = tour_repository.update_tour(
        request,
        tour_id,
        agency_id
    )

    if not tour:
        raise TourNotFoundError(
            "Tour not found or you are not authorized to update it"
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
