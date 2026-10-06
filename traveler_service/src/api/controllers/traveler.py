from fastapi import HTTPException

from schemas.get_query_request import GetQueryRequest
from services import traveler_service
from services.exceptions import (
    TravelerAlreadyExistsError,
    TravelerNotFoundError,
    ValueRequiredError,
    UnauthorizedError,
)


async def create_traveler(request):
    try:
        return await traveler_service.create_traveler(request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TravelerAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_travelers(params: GetQueryRequest = None):
    try:
        return traveler_service.get_all_travelers(params)
    except TravelerNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_traveler(traveler_id: int):
    try:
        return traveler_service.get_single_traveler(traveler_id)
    except TravelerNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_traveler(request, traveler_id: int):
    try:
        return await traveler_service.update_traveler(traveler_id, request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TravelerNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UnauthorizedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def delete_traveler(traveler_id: int):
    try:
        return await traveler_service.delete_traveler(traveler_id)
    except TravelerNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
