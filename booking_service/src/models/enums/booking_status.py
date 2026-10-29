from enum import Enum


class BookingStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    BOOKED = "booked"
    CANCELLED = "cancelled"
