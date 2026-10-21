from fastapi import HTTPException, Depends
from schemas.update_visa_request import UpdateVisaRequest
from services.exception.exceptions import ( 
    VisaNotFoundError, 
    VisaAlreadyExistsError,
    UnauthorizedError)
from repository import visa_repository
from schemas.dtos.update_visa_response import UpdateVisaResponse
from api.dependencies.authorization import get_current_agency


async def update_visa(request: UpdateVisaRequest, visa_id: int, current_agency_id: int = Depends(get_current_agency)):
    existing_visa = visa_repository.get_visa_id(visa_id)
    if not existing_visa:
        raise VisaNotFoundError("Visa application not found")
    
    if existing_visa["agency_id"] != current_agency_id:
        raise UnauthorizedError(
            "You are not authorized to update this visa"
        )

    if request.visa_name is not None:
        existing_name = visa_repository.get_visa_by_name(
            request.visa_name,
            current_agency_id
        )

        if existing_name and existing_name["id"] != visa_id:
            raise VisaAlreadyExistsError(
                "You already have a visa application with this name."
            )

    visa = visa_repository.update_visa(
        request,
        visa_id,
        current_agency_id
    )


    if not visa:
        raise VisaNotFoundError(
            "Visa not found or no longer available for update"
        )

    return UpdateVisaResponse(
        id=visa["id"],
        agency_id=visa["agency_id"],
        visa_name=visa["visa_name"],
        country=visa["country"],
        visa_type_id=visa["visa_type_id"],
        processing_time_value=visa["processing_time_value"],
        processing_time_unit=visa["processing_time_unit"],
        processing_fee=visa["processing_fee"],
        status=visa["status"],
        updated_at=visa["updated_at"]
    )