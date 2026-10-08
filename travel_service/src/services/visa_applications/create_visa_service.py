from repository import visa_repository
from models.enums.visa_status import VisaStatus
from schemas.dtos.create_visa_response import CreateVisaResponse
from schemas.create_visa_request import CreateVisaRequest
from services.exceptions import ( 
    VisaNotFoundError, 
    VisaAlreadyExistsError,
    ValueRequiredError)

async def create_new_visa(request: CreateVisaRequest, agency_id: int):
    existing_name = visa_repository.get_visa_by_name(
    request.visa_name,
    agency_id
    )

    if existing_name:
        raise VisaAlreadyExistsError(
        "You already have a visa application with this name."
    )

    status = VisaStatus.AVAILABLE
    visa = visa_repository.create(request, agency_id, status)

    return CreateVisaResponse(
        id=visa["id"],
        agency_id=visa["agency_id"],
        visa_name=visa["visa_name"],
        country=visa["country"],
        visa_type_id=visa["visa_type_id"],
        processing_time_value=visa["processing_time_value"],
        processing_time_unit=visa["processing_time_unit"],
        processing_fee=visa["processing_fee"],
        status=visa["status"],
        created_at=visa["created_at"]
    )



