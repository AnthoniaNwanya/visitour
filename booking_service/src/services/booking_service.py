from repository.booking_repository import BookingRepository


class BookingService:
    def __init__(self):
        self.repository = BookingRepository()

    async def create_booking(self, payload):
        return await self.repository.create(payload)

    async def get_all_bookings(self, params=None):
        return await self.repository.get_all(params)

    async def get_single_booking(self, booking_id: int):
        return await self.repository.get_by_id(booking_id)

    async def update_booking(self, booking_id: int, payload):
        return await self.repository.update(booking_id, payload)

    async def delete_booking(self, booking_id: int):
        return await self.repository.delete(booking_id)


booking_service = BookingService()
