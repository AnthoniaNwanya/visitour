from repository.traveler_repository import TravelerRepository


class TravelerService:
    def __init__(self):
        self.repository = TravelerRepository()

    async def create_traveler(self, payload):
        return await self.repository.create(payload)

    async def get_all_travelers(self, params=None):
        return await self.repository.get_all(params)

    async def get_single_traveler(self, traveler_id: int):
        return await self.repository.get_by_id(traveler_id)

    async def update_traveler(self, traveler_id: int, payload):
        return await self.repository.update(traveler_id, payload)

    async def delete_traveler(self, traveler_id: int):
        return await self.repository.delete(traveler_id)


traveler_service = TravelerService()
