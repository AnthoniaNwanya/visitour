from services.exceptions import ( 
    TourNotFoundError,)
from repository import travel_repository
from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency


async def delete_tour(tour_id: int, agency_id: int = Depends(get_current_agency)):
    existing_tour = travel_repository.get_tour_id(tour_id)
    if not existing_tour:
        raise TourNotFoundError("Tour not found")

    travel_repository.delete_tour(tour_id, agency_id)

    return {
        "message": "Tour was successfully deleted"
    }