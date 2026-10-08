from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class CreateVisaResponse(BaseModel):
    id: int
    agency_id: int
    visa_name: str
    country: str
    visa_type_id: int
    processing_time_value: int
    processing_time_unit: str
    processing_fee: Decimal
    status: str
    created_at: datetime
  