from enum import Enum


class TravelerStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
