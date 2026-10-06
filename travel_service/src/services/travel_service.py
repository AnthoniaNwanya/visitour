from repository.travel_repository import TravelRepository


class TravelService:
    def __init__(self):
        self.repository = TravelRepository()

    async def create_travel(self, payload):
        return await self.repository.create(payload)

    async def get_all_travels(self, params=None):
        return await self.repository.get_all(params)

    async def get_single_travel(self, travel_id: int):
        return await self.repository.get_by_id(travel_id)

    async def update_travel(self, travel_id: int, payload):
        return await self.repository.update(travel_id, payload)

    async def delete_travel(self, travel_id: int):
        return await self.repository.delete(travel_id)


travel_service = TravelService()
