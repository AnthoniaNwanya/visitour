from services.exceptions import ( 
    AgencyNotFoundError)
from repository import agency_repository

async def delete_agency(agency_id: int):
# authorize agency by logging in before this request

    existing_agency = agency_repository.get_agency_id(agency_id)
    if not existing_agency:
        raise AgencyNotFoundError("Agency not found")

    agency_repository.delete_agency(agency_id)

    return {
        "message": "Agency deleted successfully"
    }