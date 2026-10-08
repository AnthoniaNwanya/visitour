from fastapi import HTTPException, Depends
from services.exceptions import (AgencyAlreadyExistsError, 
    BadRequest,
    AgencyNotFoundError, 
    ValueRequiredError, 
    AgencyAlreadyExistsError, 
    VerifyMismatchError,
    ForbiddenError)
from schemas.agency_signup_request import AgencySignupRequest
from schemas.agency_login_request import AgencyLoginRequest
from schemas.get_query_request import GetQueryRequest
from schemas.validate_cac_request import ValidateCACRequest
from schemas.update_agency_request import UpdateAgencyRequest
from services import create_agency_service, get_agency_service, update_agency_service, delete_agency_service, cac_validation
from api.dependencies.authorization import get_current_agency

async def register_agency(request: AgencySignupRequest):

    try:
        return await create_agency_service.create_new_agency(request)

    except ValueRequiredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except AgencyAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except VerifyMismatchError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def login_agency(request: AgencyLoginRequest):
    try:
        return create_agency_service.login_agency(request)
    
    except ValueRequiredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except AgencyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except VerifyMismatchError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
    except ForbiddenError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        ) 
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def get_agencies(params: GetQueryRequest = Depends()):
    try:
        return await get_agency_service.get_all_agencies(params)
    
    except AgencyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except AgencyAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def get_agency(agency_id: int):
    try:
        return get_agency_service.get_single_agency(agency_id)

    except AgencyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def update_agency(request: UpdateAgencyRequest, agency_id: int = Depends(get_current_agency)):
    try:
        return await update_agency_service.update_agency(request, agency_id)
    
    except AgencyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except AgencyAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    except ValueRequiredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except VerifyMismatchError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def delete_agency(agency_id: int = Depends(get_current_agency)):
    try:
        return await delete_agency_service.delete_agency(agency_id)
    
    except AgencyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
async def validate_cac(agency_id: int, request: ValidateCACRequest):
    try:
        return await cac_validation.validate_cac(agency_id, request)

    except BadRequest as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 