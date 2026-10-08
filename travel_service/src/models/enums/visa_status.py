from enum import Enum


class VisaStatus(str, Enum):
    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE = "AVAILABLE"
