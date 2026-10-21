from services.exception.exceptions import ( 
    VisaNotFoundError,
    UnauthorizedError)
from repository import visa_repository
from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency


async def delete_visa(visa_id: int, current_agency_id: int = Depends(get_current_agency)):
    existing_visa = visa_repository.get_visa_id(visa_id)

    if not existing_visa:
        raise VisaNotFoundError("Visa not found")

    if existing_visa["agency_id"] != current_agency_id:
        raise UnauthorizedError(
            "You are not authorized to delete this visa"
        )

    deleted_visa = visa_repository.delete_visa(
        visa_id=visa_id,
        agency_id=current_agency_id
    )

    if not deleted_visa:
        raise VisaNotFoundError(
            "Visa could not be deleted"
        )

    return {
        "message": "Visa was successfully deleted"
    }