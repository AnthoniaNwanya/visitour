from schemas.get_visa_query_request import VisaQueryRequest
from services.exceptions import VisaNotFoundError
from repository import visa_repository
from schemas.dtos.get_visa_query_response import GetQueryResponse


async def get_all_visas(params: VisaQueryRequest):
    visas = visa_repository.get_visas(params)

    if not visas:
        raise VisaNotFoundError("Visa application with specified parameter not found")
    
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
