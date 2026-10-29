from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.enums.payment_status import PaymentStatus


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_id: int
    payment_reference: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    payment_method: str
    created_at: datetime
    updated_at: datetime
