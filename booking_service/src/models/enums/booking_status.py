from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
