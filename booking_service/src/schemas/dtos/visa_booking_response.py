from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class VisaBookingResponse(BaseModel):
    id: int
    booking_id: int
    visa_id: int
    visa_name: str
    country: str
    booking_reference: str
    traveler_id: int
    traveler_first_name: str
    traveler_last_name: str
    traveler_email: str
    quantity: int
    processing_fee: Decimal
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
