from fastapi import HTTPException

from schemas.get_query_request import GetQueryRequest
from services import booking_service
from services.exceptions import (
    BookingAlreadyExistsError,
    BookingNotFoundError,
    ValueRequiredError,
    UnauthorizedError,
)


async def create_booking(request):
    try:
        return await booking_service.create_booking(request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except BookingAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_bookings(params: GetQueryRequest = None):
    try:
        return booking_service.get_all_bookings(params)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def get_booking(booking_id: int):
    try:
        return booking_service.get_single_booking(booking_id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def update_booking(request, booking_id: int):
    try:
        return await booking_service.update_booking(booking_id, request)
    except ValueRequiredError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UnauthorizedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def delete_booking(booking_id: int):
    try:
        return await booking_service.delete_booking(booking_id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
