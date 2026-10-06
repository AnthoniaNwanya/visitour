from datetime import datetime


class BookingStatus:
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking:
    def __init__(
        self,
        id: int,
        name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
