from repository import travel_repository
from models.enums.tour_status import TourStatus
from schemas.dtos.create_tour_response import CreateTourResponse
from schemas.create_tour_request import CreateTourRequest
from services.exceptions import ( 
    TourNotFoundError, 
    TourAlreadyExistsError,
    ValueRequiredError)

async def create_new_tour(request: CreateTourRequest, agency_id: int):
    existing_title = travel_repository.get_tour_by_title(
    request.title,
    agency_id
    )

    if existing_title:
        raise TourAlreadyExistsError(
        "You already have a tour with this name."
    )

    status = TourStatus.AVAILABLE
    tour = travel_repository.create(request, agency_id, status)

    return CreateTourResponse(
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
        created_at=tour["created_at"]
    )



