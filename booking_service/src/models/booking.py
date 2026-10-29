from datetime import datetime
from decimal import Decimal

from models.enums.booking_status import BookingStatus


class Booking:
    def __init__(
        self,
        id: int,
        traveler_id: int,
        booking_reference: str,
        cart_id: int | None,
        total_amount: Decimal,
        currency: str,
        status: BookingStatus,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.traveler_id = traveler_id
        self.booking_reference = booking_reference
        self.cart_id = cart_id
        self.total_amount = total_amount
        self.currency = currency
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
