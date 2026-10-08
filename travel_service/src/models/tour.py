from datetime import datetime
from models.enums.tour_status import TourStatus

class Tour:
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        country: list[str],
        start_date: datetime,
        end_date: datetime,
        price: int,
        available_slots: int,
        status: TourStatus,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.title = title
        self.description = description
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.available_slots = available_slots
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

