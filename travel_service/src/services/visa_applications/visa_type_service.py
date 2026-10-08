from repository import visa_type_repository
from schemas.dtos.visa_type_response import VisaTypeResponse


async def get_all_visa_types():

    visa_types = visa_type_repository.get_all()

    return [
        VisaTypeResponse(
            id=visa_type["id"],
            name=visa_type["name"],
            description=visa_type["description"],
            created_at=visa_type["created_at"],
            updated_at=visa_type["updated_at"]
        )
        for visa_type in visa_types
    ]