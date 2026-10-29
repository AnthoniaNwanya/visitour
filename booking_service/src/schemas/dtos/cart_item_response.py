from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.enums.booking_type import BookingType


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_id: int
    booking_type: BookingType
    item_id: int
    item_name: str
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
