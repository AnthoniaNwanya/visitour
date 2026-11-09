from repository import traveler_repository
from schemas.dtos.get_traveler_response import GetTravelerResponse


async def get_traveler_for_agency(traveler_id: int):
    traveler = traveler_repository.get_traveler_id(traveler_id)

    if not traveler:
        return None

    return GetTravelerResponse(**traveler)
