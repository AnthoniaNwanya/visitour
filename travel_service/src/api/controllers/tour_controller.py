from fastapi import HTTPException, Depends
from api.dependencies.authorization import get_current_agency
from schemas.get_query_request import GetQueryRequest
from schemas.create_tour_request import CreateTourRequest
from schemas.update_tour_request import UpdateTourRequest
from services.tours import create_tour_service, get_tour_service, update_tour_service, delete_tour_service
from services.exceptions import (
    TourAlreadyExistsError,
    TourNotFoundError,
    ValueRequiredError,
    UnauthorizedError,
)


async def create_tour(request: CreateTourRequest, agency_id: int = Depends(get_current_agency) ):
    try:
        return await create_tour_service.create_new_tour(request, agency_id)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TourAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def get_tours(
        params: GetQueryRequest = Depends()):
        # ,
        # current_user: dict = Depends(get_current_user)):
    try:
        return await get_tour_service.get_all_tours(params) #, current_user["role"])
    except TourNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_tour(tour_id: int):
    try:
        return tour_service.get_single_tour(tour_id)
    except TourNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_tour(request: UpdateTourRequest, tour_id: int, agency_id: int = Depends(get_current_agency)):
    try:
        return await update_tour_service.update_tour(request, tour_id, agency_id )
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TourNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UnauthorizedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def delete_tour(tour_id: int, agency_id: int = Depends(get_current_agency)):
    try:
        return await delete_tour_service.delete_tour(tour_id, agency_id)
    except TourNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
