from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class UpdateVisaRequest(BaseModel):
    visa_name: str | None = None
    country: str | None = None
    visa_type_id: int | None = None
    processing_time_value: int | None = None
    processing_time_unit: str | None = None
    processing_fee: Decimal | None = None
    status: str | None = None

