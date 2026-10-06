from fastapi import HTTPException

from schemas.get_query_request import GetQueryRequest
from services import tour_service
from services.exceptions import (
    TravelAlreadyExistsError,
    TravelNotFoundError,
    ValueRequiredError,
    UnauthorizedError,
)


async def create_tours(request):
    try:
        return await travel_service.create_tour(request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TravelAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_tours(params: GetQueryRequest = None):
    try:
        return tour_service.get_all_tours(params)
    except TravelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_tour(tour_id: int):
    try:
        return tour_service.get_single_tour(tour_id)
    except TravelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_tour(request, travel_id: int):
    try:
        return await tour_service.update_tour(tour_id, request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TravelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UnauthorizedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def delete_tour(tour_id: int):
    try:
        return await tour_service.delete_tour(tour_id)
    except TravelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
