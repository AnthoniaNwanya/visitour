from datetime import datetime
from decimal import Decimal

from models.enums.booking_type import BookingType


class CartItem:
    def __init__(
        self,
        id: int,
        cart_id: int,
        booking_type: BookingType,
        item_id: int,
        item_name: str,
        quantity: int,
        unit_price: Decimal,
        total_amount: Decimal,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.cart_id = cart_id
        self.booking_type = booking_type
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.created_at = created_at
        self.updated_at = updated_at
