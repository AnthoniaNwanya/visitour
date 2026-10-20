from services.exception.exceptions import ( 
    TravelerNotFoundError,
    UnauthorizedError)
from repository import traveler_repository

async def delete_traveler(current_traveler_id: int):
    existing_traveler = traveler_repository.get_traveler_id(
        current_traveler_id
    )
    if not existing_traveler:
        raise TravelerNotFoundError("Traveler not found")

    traveler_repository.delete_traveler(current_traveler_id)

    return {
        "message": "Traveler was successfully deleted"
    }