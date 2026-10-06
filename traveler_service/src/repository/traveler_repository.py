class TravelerRepository:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection

    async def get_all(self, params=None):
        return []

    async def get_by_id(self, traveler_id: int):
        return None

    async def create(self, payload):
        return payload

    async def update(self, traveler_id: int, payload):
        return payload

    async def delete(self, traveler_id: int):
        return True
