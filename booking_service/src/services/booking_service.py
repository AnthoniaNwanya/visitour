from schemas.dtos.booking_response import BookingResponse
from schemas.dtos.tour_booking_response import TourBookingResponse
from schemas.dtos.visa_booking_response import VisaBookingResponse
from repository.booking_repository import BookingRepository
from repository.cart_repository import CartRepository


class BookingService:
    def __init__(self):
        self.booking_repository = BookingRepository()
        self.cart_repository = CartRepository()

    async def get_traveler_bookings(
        self, traveler_id: int
    ) -> list[BookingResponse]:
        bookings = await self.booking_repository.get_all(traveler_id)
        return [BookingResponse.model_validate(dict(row)) for row in bookings]

    async def get_agency_tour_bookings(
        self, agency_id: int
    ) -> list[TourBookingResponse]:
        bookings = await self.booking_repository.get_agency_tour_bookings(
            agency_id
        )
        return [TourBookingResponse.model_validate(dict(row)) for row in bookings]

    async def get_agency_visa_bookings(
        self, agency_id: int
    ) -> list[VisaBookingResponse]:
        bookings = await self.booking_repository.get_agency_visa_bookings(
            agency_id
        )
        return [VisaBookingResponse.model_validate(dict(row)) for row in bookings]

    async def finalize_paid_cart(
        self, cart_id: int
    ) -> list[BookingResponse]:
        """Finalize only from trusted backend code, never from a client request."""
        bookings = await self.cart_repository.finalize_paid_cart(cart_id)
        return [BookingResponse.model_validate(dict(row)) for row in bookings]


booking_service = BookingService()
