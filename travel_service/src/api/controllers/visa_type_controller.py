from services.visa_applications import visa_type_service


async def get_visa_types():
    return await visa_type_service.get_all_visa_types()