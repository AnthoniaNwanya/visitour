from fastapi import Depends

from api.dependencies.authorization import get_current_agency
from schemas.dtos.tour_booking_response import TourBookingResponse
from schemas.dtos.visa_booking_response import VisaBookingResponse
from services.booking_service import booking_service


async def get_tour_bookings(
    agency_id: int = Depends(get_current_agency),
) -> list[TourBookingResponse]:
    return await booking_service.get_agency_tour_bookings(agency_id)


async def get_visa_bookings(
    agency_id: int = Depends(get_current_agency),
) -> list[VisaBookingResponse]:
    return await booking_service.get_agency_visa_bookings(agency_id)
