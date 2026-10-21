from schemas.get_visa_query_request import VisaQueryRequest
from services.exception.exceptions import VisaNotFoundError
from repository import visa_repository
from schemas.dtos.get_visa_query_response import GetQueryResponse
from models.enums.visa_status import VisaStatus


async def get_other_agency_visas(params: VisaQueryRequest,
    current_agency_id: int):
    visas = visa_repository.get_visas_for_agency_browsing(params, current_agency_id=current_agency_id)

    if not visas:
        raise VisaNotFoundError("No visas found with the specified parameters")
    
    return [
        GetQueryResponse(
            id=visa["id"],
            agency_id=visa["agency_id"],
            visa_name=visa["visa_name"],
            country=visa["country"],
            visa_type_id=visa["visa_type_id"],
            processing_time_value=visa["processing_time_value"],
            processing_time_unit=visa["processing_time_unit"],
            processing_fee=visa["processing_fee"],
            status=visa["status"],
            created_at=visa["created_at"],
            updated_at= visa["updated_at"]
        )

        for visa in visas
    ]

async def get_available_visas(params):
    visas = visa_repository.get_visas(
        params,
        status=VisaStatus.AVAILABLE
    )
    if not visas:
        raise VisaNotFoundError("Visa with specified parameter not found")
    
    return [
        GetQueryResponse(
            id=visa["id"],
            agency_id=visa["agency_id"],
            visa_name=visa["visa_name"],
            country=visa["country"],
            visa_type_id=visa["visa_type_id"],
            processing_time_value=visa["processing_time_value"],
            processing_time_unit=visa["processing_time_unit"],
            processing_fee=visa["processing_fee"],
            status=visa["status"],
            created_at=visa["created_at"],
            updated_at= visa["updated_at"]
        )
        for visa in visas
    ]


async def get_agency_visas(params, agency_id):
    visas = visa_repository.get_visas(
        params,
        agency_id=agency_id
    )
    if not visas:
        raise VisaNotFoundError("Visa with specified parameter not found")

    return [
        GetQueryResponse(
            id=visa["id"],
            agency_id=visa["agency_id"],
            visa_name=visa["visa_name"],
            country=visa["country"],
            visa_type_id=visa["visa_type_id"],
            processing_time_value=visa["processing_time_value"],
            processing_time_unit=visa["processing_time_unit"],
            processing_fee=visa["processing_fee"],
            status=visa["status"],
            created_at=visa["created_at"],
            updated_at= visa["updated_at"]
        )
        for visa in visas
        ]
