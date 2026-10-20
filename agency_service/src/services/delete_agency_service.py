from services.exception.exceptions import ( 
    AgencyNotFoundError)
from repository import agency_repository

async def delete_agency(current_agency_id: int):
    existing_agency = agency_repository.get_agency_id(current_agency_id)
    if not existing_agency:
        raise AgencyNotFoundError("Agency not found")

    agency_repository.delete_agency(current_agency_id)

    return {
        "message": "Agency deleted successfully"
    }