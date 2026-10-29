from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.enums.cart_status import CartStatus
from schemas.dtos.cart_item_response import CartItemResponse


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    traveler_id: int
    status: CartStatus
    total_order_summary: Decimal
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse]
