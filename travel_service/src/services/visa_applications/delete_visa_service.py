from services.exceptions import ( 
    VisaNotFoundError,)
from repository import visa_repository
from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency


async def delete_visa(visa_id: int, agency_id: int = Depends(get_current_agency)):
    existing_visa = visa_repository.get_visa_id(visa_id)
    if not existing_visa:
        raise VisaNotFoundError("Visa not found")

    visa_repository.delete_visa(visa_id, agency_id)

    return {
        "message": "Visa was successfully deleted"
    }