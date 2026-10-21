from fastapi import HTTPException, Depends
from services.exception.exceptions import (
    TravelerAlreadyExistsError, 
    TravelerNotFoundError, 
    ValueRequiredError, 
    VerifyMismatchError,
    ForbiddenError)
from schemas.traveler_signup_request import TravelerSignupRequest
from schemas.traveler_login_request import TravelerLoginRequest
from schemas.get_traveler_query_request import GetTravelerQueryRequest
from schemas.update_traveler_request import UpdateTravelerRequest
from services import (create_traveler_service,
    get_traveler_service, 
    update_traveler_service,
    delete_traveler_service)
from api.dependencies.authorization import get_current_traveler, get_current_user

async def register_traveler(request: TravelerSignupRequest):

    try:
        return await create_traveler_service.create_traveler(request)

    except ValueRequiredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except TravelerAlreadyExistsError as e:
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


def login_traveler(request: TravelerLoginRequest):
    try:
        return create_traveler_service.login_traveler(request)
    
    except ValueRequiredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except TravelerNotFoundError as e:
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

async def get_travelers(params: GetTravelerQueryRequest = Depends()):
    try:
        return await get_traveler_service.get_travelers(params)
    
    except ForbiddenError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
    except TravelerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except TravelerAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def get_traveler_for_traveler(current_traveler_id: int = Depends(get_current_traveler)):
    try:
        return await get_traveler_service.get_traveler_for_traveler(current_traveler_id)
    
    except ForbiddenError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
    except TravelerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def get_traveler_for_agency(traveler_id:int, current_user: dict = Depends(get_current_user)):
    try:
        agency_id = current_user["id"]
        role = current_user["role"]

        if role != "agency":
            raise HTTPException(
                status_code=403,
                detail="Only agencies can access traveler details"
            )
        
        return await get_traveler_service.get_traveler_for_agency(traveler_id)
    
    except ForbiddenError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
    except TravelerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except TravelerAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def update_traveler(request: UpdateTravelerRequest, current_traveler_id: int = Depends(get_current_traveler)):
    try:
        return await update_traveler_service.update_traveler(request, current_traveler_id=current_traveler_id)
    
    except TravelerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except TravelerAlreadyExistsError as e:
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


async def delete_traveler(current_traveler_id: int = Depends(get_current_traveler)):
    try:
        return await delete_traveler_service.delete_traveler(
            current_traveler_id=current_traveler_id)
    
    except TravelerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
