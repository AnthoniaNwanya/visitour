from datetime import datetime
from decimal import Decimal

from models.enums.cart_status import CartStatus


class Cart:
    def __init__(
        self,
        id: int,
        traveler_id: int,
        status: CartStatus,
        total_order_summary: Decimal,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.traveler_id = traveler_id
        self.status = status
        self.total_order_summary = total_order_summary
        self.created_at = created_at
        self.updated_at = updated_at
