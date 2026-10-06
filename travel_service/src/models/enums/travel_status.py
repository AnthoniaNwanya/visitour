from enum import Enum


class TravelStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
