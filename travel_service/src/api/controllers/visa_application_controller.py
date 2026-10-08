from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency
from schemas.get_visa_query_request import VisaQueryRequest
from schemas.create_visa_request import CreateVisaRequest
from schemas.update_visa_request import UpdateVisaRequest
from services.visa_applications import create_visa_service, get_visa_service, update_visa_service, delete_visa_service
from services.exceptions import (
    VisaAlreadyExistsError,
    VisaNotFoundError,
    ValueRequiredError,
    UnauthorizedError,
)


async def create_visa_application(request: CreateVisaRequest, agency_id: int = Depends(get_current_agency) ):
    try:
        return await create_visa_service.create_new_visa(request, agency_id)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except VisaAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def get_visa_applications(
        params: VisaQueryRequest = Depends()):
        # ,
        # current_user: dict = Depends(get_current_user)):
    try:
        return await get_visa_service.get_all_visas(params) #, current_user["role"])
    except VisaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_visa_application(request: UpdateVisaRequest, visa_id: int, agency_id: int = Depends(get_current_agency)):
    try:
        return await update_visa_service.update_visa(request, visa_id, agency_id )
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except VisaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UnauthorizedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def delete_visa_application(visa_id: int, agency_id: int = Depends(get_current_agency)):
    try:
        return await delete_visa_service.delete_visa(visa_id, agency_id)
    except VisaNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
