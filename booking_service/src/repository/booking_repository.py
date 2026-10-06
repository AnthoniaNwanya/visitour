class BookingRepository:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection

    async def get_all(self, params=None):
        return []

    async def get_by_id(self, booking_id: int):
        return None

    async def create(self, payload):
        return payload

    async def update(self, booking_id: int, payload):
        return payload

    async def delete(self, booking_id: int):
        return True
