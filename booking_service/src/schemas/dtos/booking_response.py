from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.enums.booking_status import BookingStatus


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    traveler_id: int
    cart_id: int | None
    booking_reference: str
    total_amount: Decimal
    currency: str
    status: BookingStatus
    created_at: datetime
    updated_at: datetime
