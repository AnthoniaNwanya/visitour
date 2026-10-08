from fastapi import HTTPException, Depends
from schemas.update_visa_request import UpdateVisaRequest
from services.exceptions import ( 
    VisaNotFoundError, 
    VisaAlreadyExistsError)
from repository import visa_repository
from schemas.dtos.update_visa_response import UpdateVisaResponse
from api.dependencies.authorization import get_current_agency


async def update_visa(request: UpdateVisaRequest, visa_id: int, agency_id: int = Depends(get_current_agency)):
    existing_id = visa_repository.get_visa_id(visa_id)
    if not existing_id:
        raise VisaNotFoundError("Visa application not found")

    existing_name = visa_repository.get_visa_by_name(
        request.visa_name,
        agency_id
    )

    if existing_name and existing_name["id"] != visa_id:
        raise VisaAlreadyExistsError(
            "You already have a visa application with this name."
        )

    visa = visa_repository.update_visa(
        request,
        visa_id
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