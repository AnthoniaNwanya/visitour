from datetime import datetime
from decimal import Decimal


class TourBooking:
    def __init__(
        self,
        id: int,
        booking_id: int,
        tour_id: int,
        agency_id: int,
        tour_name: str,
        quantity: int,
        unit_price: Decimal,
        total_amount: Decimal,
        status: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.booking_id = booking_id
        self.tour_id = tour_id
        self.agency_id = agency_id
        self.tour_name = tour_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
