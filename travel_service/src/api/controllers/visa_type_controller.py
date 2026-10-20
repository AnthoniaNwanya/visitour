from services.visa_applications import visa_type_service
from fastapi import HTTPException, Depends


async def get_visa_types():
    try: 
        return await visa_type_service.get_all_visa_types()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc