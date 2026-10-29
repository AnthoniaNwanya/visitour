from fastapi import Depends

from api.dependencies.authorization import get_current_traveler
from schemas.dtos.booking_response import BookingResponse
from services.booking_service import booking_service


async def get_bookings(
    traveler_id: int = Depends(get_current_traveler),
) -> list[BookingResponse]:
    return await booking_service.get_traveler_bookings(traveler_id)
