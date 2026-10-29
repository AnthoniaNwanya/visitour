from datetime import datetime
from decimal import Decimal


class VisaBooking:
    def __init__(
        self,
        id: int,
        booking_id: int,
        visa_id: int,
        agency_id: int,
        visa_name: str,
        country: str,
        quantity: int,
        processing_fee: Decimal,
        total_amount: Decimal,
        status: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.booking_id = booking_id
        self.visa_id = visa_id
        self.agency_id = agency_id
        self.visa_name = visa_name
        self.country = country
        self.quantity = quantity
        self.processing_fee = processing_fee
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
