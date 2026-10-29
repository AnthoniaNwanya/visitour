from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TourBookingResponse(BaseModel):
    id: int
    booking_id: int
    tour_id: int
    tour_name: str
    booking_reference: str
    traveler_id: int
    traveler_first_name: str
    traveler_last_name: str
    traveler_email: str
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
