from enum import Enum


class TourStatus(str, Enum):
    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE = "AVAILABLE"
    IN_PROGRESS = "IN_PROGRESS"
