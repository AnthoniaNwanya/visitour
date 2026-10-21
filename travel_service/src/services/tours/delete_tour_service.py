from services.exception.exceptions import ( 
    TourNotFoundError,
    UnauthorizedError)
from repository import tour_repository
from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency


async def delete_tour(tour_id: int, agency_id: int = Depends(get_current_agency)):
    existing_tour = tour_repository.get_tour_id(tour_id)

    if not existing_tour:
        raise TourNotFoundError("Tour not found")

    if existing_tour["agency_id"] != agency_id:
        raise UnauthorizedError(
            "You are not authorized to delete this tour"
        )

    deleted_tour = tour_repository.delete_tour(
        tour_id=tour_id,
        agency_id=agency_id
    )

    if not deleted_tour:
        raise TourNotFoundError(
            "Tour could not be deleted"
        )
    return {
        "message": "Tour was successfully deleted"
    }